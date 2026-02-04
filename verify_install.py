#!/usr/bin/env python3
# Copyright 2026 The Civilis Authors
# Licensed under Apache License 2.0

"""
Quick verification script for Civilis installation.
Run: python verify_install.py
"""

import sys
import traceback

def check_imports():
    print("🔍 Checking imports...")
    try:
        import civilis
        from civilis import CivilisSimulation, CivilisAgent
        print(f"✅ Civilis {civilis.__version__} imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def run_mini_simulation():
    print("\n🧪 Running minimal simulation test...")
    try:
        sim = CivilisSimulation(num_agents=5, rounds=10, seed=42)
        history = sim.run()
        assert len(history) > 0
        assert "round" in history[0]
        print(f"✅ Simulation completed ({len(history)} checkpoints)")
        print(f"   Final insights: {history[-1]['total_insights']}")
        return True
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("="*50)
    print("CIVILIS INSTALLATION VERIFICATION")
    print("="*50)
    
    checks = [
        ("Import check", check_imports),
        ("Simulation test", run_mini_simulation)
    ]
    
    all_passed = True
    for name, check_fn in checks:
        try:
            if not check_fn():
                all_passed = False
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Civilis is ready to use.")
        print("\nNext steps:")
        print("  • Try examples/civilization_100.py")
        print("  • Open examples/colab_demo.ipynb in Google Colab")
        print("  • Explore docs/ for API reference")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED. Please review errors above.")
        print("\nTroubleshooting:")
        print("  • Run: pip install -e '.[dev]'")
        print("  • Check GitHub Issues: https://github.com/civilis-ai/civilis/issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())