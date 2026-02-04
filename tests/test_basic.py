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

import pytest
from civilis.core import CivilisAgent
from civilis.simulation import CivilisSimulation

def test_agent_creation():
    agent = CivilisAgent("A001")
    assert agent.id == "A001"
    assert len(agent.memory.insights) == 0

def test_agent_learning():
    agent = CivilisAgent("A002")
    agent.learn("Fire is dangerous.", "Xun")
    assert len(agent.memory.insights) == 1
    assert agent.memory.insights[0].content == "Fire is dangerous."

def test_simulation_run():
    sim = CivilisSimulation(num_agents=10, rounds=10, seed=123)
    history = sim.run()
    assert len(history) > 0
    assert "round" in history[0]
    assert "total_insights" in history[0]
    assert history[-1]["round"] == 10