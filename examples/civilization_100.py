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

"""
Example: Run a 100-agent civilization simulation and plot results.
"""

import json
import matplotlib.pyplot as plt
from civilis import CivilisSimulation

def main():
    sim = CivilisSimulation(num_agents=100, rounds=500, seed=42)
    history = sim.run()

    # Save results
    with open("civilization_100.json", "w") as f:
        json.dump(history, f, indent=2)

    # Plot
    rounds = [h["round"] for h in history]
    diversity = [h["diversity"] for h in history]
    consensus = [h["consensus"] for h in history]

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(rounds, diversity, 'b-o')
    plt.title("Knowledge Diversity")
    plt.xlabel("Round")
    plt.ylabel("Diversity")

    plt.subplot(1, 2, 2)
    plt.plot(rounds, consensus, 'r-o')
    plt.title("Group Consensus")
    plt.xlabel("Round")
    plt.ylabel("Top-5 Consensus Ratio")

    plt.tight_layout()
    plt.savefig("civilization_100.png", dpi=150)
    print("✅ Results saved to civilization_100.json and civilization_100.png")

if __name__ == "__main__":
    main()