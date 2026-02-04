# Civilis 🌍

[![CI](https://github.com/civilis-ai/civilis/workflows/CI/badge.svg)](https://github.com/civilis-ai/civilis/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/civilis)](https://pypi.org/project/civilis/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/civilis-ai/civilis/blob/main/examples/colab_demo.ipynb)

> A cognitive architecture for embodied agents, validated through multi-agent civilization simulation.

...

## 📦 Install
## 🔒 Offline Usage (Restricted Networks)

Civilis fully supports offline operation for environments with:
- Corporate firewalls
- Air-gapped systems
- China mainland networks (Great Firewall)
- CI/CD pipelines without internet

### ✅ Automatic Offline Detection
No configuration needed! Civilis automatically:
1. Checks `CIVILIS_OFFLINE=1` or `TRANSFORMERS_OFFLINE=1` environment variables
2. Performs lightweight network test (1-second timeout)
3. Falls back to synthetic embeddings if network unavailable

### 🚀 Manual Offline Mode (Recommended for Verification)
```bash
# Linux/macOS
export CIVILIS_OFFLINE=1
python verify_install.py

# Windows PowerShell
 $ env:CIVILIS_OFFLINE=1; python verify_install.py

# Windows CMD
set CIVILIS_OFFLINE=1 && python verify_install.py

### ✅ Recommended (works today):
```bash
pip install git+https://github.com/civilis-ai/civilis.git

> Simulate the emergence of artificial civilizations through insight-based multi-agent learning.

Civilis is an open-source framework for modeling how simple agents, equipped with modular cognition (inspired by octopus neurology and Eastern philosophy), can collectively evolve culture, consensus, and innovation.

![Civilization Metrics](https://raw.githubusercontent.com/civilis-ai/civilis/main/docs/metrics.png)

## ✨ Features
- 🐙 **Octo-Architecture**: 8 specialized modules + 1 central hub
- 💡 **Insight-Based Learning**: Knowledge emerges via repetition & reflection
- 🌐 **Small-World Society**: Realistic social network dynamics
- 📊 **Civilization Metrics**: Track diversity, consensus, innovation

## 🚀 Quick Start (Colab)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/civilis-ai/civilis/blob/main/examples/colab_demo.ipynb)

## 📦 Install
```bash
pip install civilis