# Copyright 2024 Civilis Contributors
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
"""
Civilis Simulation Core
支持：HuggingFace镜像（中国大陆优化）| 本地模型路径 | 清晰错误指引
无需修改代码，通过环境变量灵活配置
"""
import numpy as np
import os
from typing import List, Dict, Any

# =============== CivilisAgent 类 ===============
class CivilisAgent:
    def __init__(self, agent_id: int, embedding_model, rng: np.random.Generator):
        self.agent_id = agent_id
        self.embedding_model = embedding_model
        self.rng = rng
        self.memory = []
        self.insights = 0
    
    def observe(self, observation: str):
        self.memory.append(observation)
    
    def reflect(self) -> str:
        if not self.memory:
            return "No observations yet"
        recent = self.memory[-3:]
        self.insights += 1
        return f"Insight #{self.insights}: Based on {len(recent)} observations"

# =============== CivilisSimulation 核心类 ===============
class CivilisSimulation:
    def __init__(self, num_agents: int = 10, rounds: int = 100, seed: int = None):
        self.num_agents = num_agents
        self.rounds = rounds
        self.seed = seed if seed is not None else np.random.randint(0, 10000)
        self.rng = np.random.default_rng(self.seed)
        self._init_embedding()
        self.agents = [CivilisAgent(i, self.embedding_model, self.rng) for i in range(self.num_agents)]
        self.history = []
    
    def _init_embedding(self):
        model_path = os.getenv(
            "CIVILIS_EMBEDDING_MODEL", 
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # 中国大陆网络优化（自动启用HF镜像）
        if "sentence-transformers/" in model_path and os.getenv("HF_ENDPOINT") is None:
            try:
                import socket
                socket.setdefaulttimeout(2.0)
                socket.create_connection(("hf-mirror.com", 443), timeout=2)
                os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
                print("🌐 检测到中国大陆网络环境，已自动启用HuggingFace镜像源 (hf-mirror.com)")
            except:
                pass
        
        try:
            print(f"📥 正在加载嵌入模型: {model_path}")
            from sentence_transformers import SentenceTransformer
            
            self.embedding_model = SentenceTransformer(
                model_path,
                trust_remote_code=True,
                cache_folder=os.getenv("CIVILIS_MODEL_CACHE", None)
            )
            dim = self.embedding_model.get_sentence_embedding_dimension()
            print(f"✅ 模型加载成功 | 维度: {dim} | 来源: {model_path}")
            
        except Exception as e:
            error_msg = f"""
❌ 模型加载失败: {str(e)}

💡 解决方案（任选其一）:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【方案1】启用HuggingFace镜像（中国大陆推荐）
   Windows PowerShell:
      $env:HF_ENDPOINT="https://hf-mirror.com"; python verify_install.py
   
   Windows CMD:
      set HF_ENDPOINT=https://hf-mirror.com && python verify_install.py
   
   Git Bash / Linux / macOS:
      export HF_ENDPOINT=https://hf-mirror.com
      python verify_install.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【方案2】手动下载模型（100%可靠）
   1. 创建模型目录: mkdir -p ./models/embeddings
   2. 下载模型（使用镜像）:
        git lfs install
        git clone https://hf-mirror.com/sentence-transformers/all-MiniLM-L6-v2 ./models/embeddings
   3. 设置环境变量:
        export CIVILIS_EMBEDDING_MODEL=./models/embeddings
   4. 重新运行: python verify_install.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            print(error_msg)
            raise RuntimeError("嵌入模型加载失败，请根据上方指引操作") from e
    
    def run(self) -> Dict[str, Any]:
        print(f"🌍 初始化 Civilis 模拟 ({self.num_agents} 智能体, {self.rounds} 轮)...")
        
        for round_num in range(self.rounds):
            observations = [f"Round {round_num} observation" for _ in range(self.num_agents)]
            reflections = []
            for agent, obs in zip(self.agents, observations):
                agent.observe(obs)
                reflections.append(agent.reflect())
            
            self.history.append({
                "round": round_num,
                "observations": observations,
                "reflections": reflections
            })
        
        total_insights = sum(agent.insights for agent in self.agents)
        print(f"✅ 模拟完成! 总洞察数: {total_insights}")
        
        return {
            "total_insights": total_insights,
            "agents_count": self.num_agents,
            "rounds_completed": self.rounds,
            "history_length": len(self.history),
            "history": self.history
        }
    
    def get_agent_insights(self, agent_id: int) -> int:
        if 0 <= agent_id < len(self.agents):
            return self.agents[agent_id].insights
        return 0
