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

import random
import networkx as nx
from collections import Counter
from typing import List, Dict, Any
from .core import CivilisAgent

class CivilisSimulation:
    """
    Simulate an artificial civilization of insight-based agents.
    
    Args:
        num_agents: Number of agents in the society (min=1)
        rounds: Total simulation rounds (min=1)
        network_type: 'small_world' (default) or 'random'
        seed: Random seed for reproducibility
    """

    def __init__(
        self,
        num_agents: int = 50,
        rounds: int = 300,
        network_type: str = "small_world",
        seed: int = 42
    ):
        if num_agents < 1:
            raise ValueError("num_agents must be at least 1")
        if rounds < 1:
            raise ValueError("rounds must be at least 1")
        
        self.num_agents = num_agents
        self.rounds = rounds
        self.network_type = network_type
        self.seed = seed
        random.seed(seed)

    def _build_network(self) -> nx.Graph:
        if self.network_type == "small_world":
            G = nx.watts_strogatz_graph(self.num_agents, 4, 0.2, seed=self.seed)
        else:
            G = nx.gnm_random_graph(self.num_agents, self.num_agents * 2, seed=self.seed)
        mapping = {i: f"A{i:03d}" for i in range(self.num_agents)}
        return nx.relabel_nodes(G, mapping)

    def run(self) -> List[Dict[str, Any]]:
        print(f"🌍 Initializing Civilis simulation ({self.num_agents} agents, {self.rounds} rounds)...")
        
        agents = [CivilisAgent(f"A{i:03d}") for i in range(self.num_agents)]
        id_to_agent = {a.id: a for a in agents}
        G = self._build_network()

        common_knowledge = ["Fire is dangerous.", "Water helps survival.", "Sharing is beneficial."]
        for agent in agents:
            for k in common_knowledge:
                agent.learn(k, "Kun")

        history = []
        LOG_INTERVAL = max(1, self.rounds // 10)

        for round_num in range(1, self.rounds + 1):
            num_speakers = max(1, min(int(0.3 * self.num_agents), len(agents)))
            speakers = random.sample(agents, k=num_speakers)
            
            for speaker in speakers:
                neighbors = list(G.neighbors(speaker.id))
                if not neighbors:
                    continue
                listener = id_to_agent[random.choice(neighbors)]
                msg = random.choice(common_knowledge + ["I wonder about cooperation."])
                listener.interact(msg)

            if round_num % LOG_INTERVAL == 0 or round_num == 1:
                all_insights = [ins.content for a in agents for ins in a.memory.insights]
                unique = set(all_insights)
                diversity = len(unique) / max(len(all_insights), 1)
                counter = Counter(all_insights)
                top5 = sum(c for _, c in counter.most_common(5))
                consensus = top5 / max(len(all_insights), 1)
                metrics = {
                    "round": round_num,
                    "total_insights": len(all_insights),
                    "diversity": round(diversity, 4),
                    "consensus": round(consensus, 4)
                }
                history.append(metrics)
                
                if round_num == 1 or round_num % (LOG_INTERVAL * 2) == 0:
                    print(f"  🔄 Round {round_num}/{self.rounds} | Insights: {len(all_insights)} | Diversity: {diversity:.2f}")

        print(f"✅ Simulation completed! Final insights: {history[-1]['total_insights']}")
        return history