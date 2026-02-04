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
嵌入模型后端抽象层
支持：Sentence-Transformers | 未来扩展 Ollama/LocalAI 等
"""
import os
from typing import Any, Optional

class EmbeddingBackend:
    """嵌入模型后端基类"""
    def encode(self, texts: list[str]) -> Any:
        raise NotImplementedError
    
    def get_dimension(self) -> int:
        raise NotImplementedError

class SentenceTransformerBackend(EmbeddingBackend):
    """Sentence-Transformers 后端实现（当前默认）"""
    def __init__(self, model_path: str, cache_folder: Optional[str] = None):
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
        
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(
            model_path,
            trust_remote_code=True,
            cache_folder=cache_folder
        )
    
    def encode(self, texts: list[str]) -> Any:
        return self.model.encode(texts, convert_to_tensor=True)
    
    def get_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

def get_embedding_backend(
    model_path: str = "sentence-transformers/all-MiniLM-L6-v2",
    backend_type: str = "sentence-transformers",
    cache_folder: Optional[str] = None
) -> EmbeddingBackend:
    """工厂函数：根据配置返回嵌入后端实例"""
    if backend_type == "sentence-transformers":
        return SentenceTransformerBackend(model_path, cache_folder)
    raise ValueError(f"Unsupported backend type: {backend_type}")
