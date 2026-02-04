# Copyright 2026 The Civilis Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import numpy as np
from typing import List, Optional
from dataclasses import dataclass, field

# Lazy imports to avoid heavy load at module level
_embedding_model = None
_llm_pipeline = None

def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return _embedding_model

def _get_llm():
    global _llm_pipeline
    if _llm_pipeline is None:
        from transformers import pipeline
        _llm_pipeline = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True
        )
    return _llm_pipeline

@dataclass
class Insight:
    content: str
    vector: np.ndarray
    strength: int = 1
    last_used: float = field(default_factory=time.time)
    source_module: str = "unknown"

class VectorMemory:
    def __init__(self, max_insights: int = 200):
        self.insights: List[Insight] = []
        self.max_insights = max_insights

    def add_insight(self, content: str, source_module: str = "unknown"):
        for ins in self.insights:
            if ins.content == content:
                ins.strength += 1
                ins.last_used = time.time()
                return
        vec = _get_embedding_model().encode(content)
        self.insights.append(Insight(content=content, vector=vec, source_module=source_module))
        if len(self.insights) > self.max_insights:
            self.insights.sort(key=lambda x: (x.strength, x.last_used))
            self.insights.pop(0)

    def query(self, text: str, top_k: int = 2, threshold: float = 0.5) -> List[Insight]:
        q_vec = _get_embedding_model().encode(text)
        scored = []
        for ins in self.insights:
            sim = float(np.dot(q_vec, ins.vector) / (np.linalg.norm(q_vec) * np.linalg.norm(ins.vector)))
            if sim >= threshold:
                scored.append((sim, ins))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [ins for _, ins in scored[:top_k]]

class CivilisAgent:
    def __init__(self, agent_id: str):
        self.id = agent_id
        self.memory = VectorMemory()
        self.insight_threshold = 4

    def learn(self, statement: str, source_module: str = "Xun"):
        self.memory.add_insight(statement, source_module)
        matches = self.memory.query(statement, top_k=1, threshold=0.95)
        if matches and matches[0].strength >= self.insight_threshold:
            print(f"[{self.id}] 💡 INSIGHT: {statement}")

    def interact(self, message: str) -> str:
        # In full version, this would call LLM for response
        # For lightweight simulation, we skip generation and focus on learning
        self.learn(message)
        return f"[{self.id}] Acknowledged."