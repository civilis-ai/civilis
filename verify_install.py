#!/usr/bin/env python3
# Copyright 2026 The Civilis Authors
# Licensed under Apache License 2.0

"""
Civilis Installation Verifier
Detects common setup issues and provides exact fixes.
"""

import sys
import os
import subprocess
from pathlib import Path
import traceback

def check_project_structure():
    """验证关键文件是否存在及正确性"""
    issues = []
    
    # 1. 检查核心文件存在
    critical_files = [
        "pyproject.toml",
        "src/civilis/__init__.py",
        "src/civilis/core.py",
        "src/civilis/simulation.py"
    ]
    
    for f in critical_files:
        if not Path(f).exists():
            issues.append(f"❌ Missing critical file: {f}")
    
    # 2. 检查 __init__.py 内容
    init_path = Path("src/civilis/__init__.py")
    if init_path.exists():
        content = init_path.read_text(encoding='utf-8')
        required_imports = ["CivilisAgent", "CivilisSimulation"]
        for imp in required_imports:
            if imp not in content:
                issues.append(f"❌ {init_path} missing export: {imp}")
    
    # 3. 检查是否在项目根目录
    if not Path("pyproject.toml").exists():
        issues.append("❌ Not in project root directory! pyproject.toml not found")
        issues.append("💡 Navigate to the directory containing pyproject.toml")
    
    return issues

def check_installation():
    """尝试导入并运行最小测试"""
    try:
        import civilis
        from civilis import CivilisAgent, CivilisSimulation
        
        # 验证版本号存在
        if not hasattr(civilis, "__version__"):
            return ["❌ civilis.__version__ not defined"]
        
        # 运行微型模拟
        sim = CivilisSimulation(num_agents=5, rounds=3, seed=42)
        history = sim.run()
        
        if not history or len(history) == 0:
            return ["❌ Simulation returned empty history"]
        
        return []  # 无问题
    
    except Exception as e:
        return [f"❌ Runtime error: {str(e)}", traceback.format_exc()]

def print_fix_instructions(issues):
    """生成精确的修复命令"""
    print("\n🔧 AUTOMATED FIX INSTRUCTIONS")
    print("="*50)
    
    if any("Not in project root" in i for i in issues):
        print("1. NAVIGATE TO PROJECT ROOT:")
        print("   cd /path/to/civilis  # Where pyproject.toml lives")
    
    if any("Missing critical file" in i for i in issues):
        print("\n2. RESTORE MISSING FILES:")
        print("   git checkout -- src/civilis/__init__.py")
        print("   git checkout -- src/civilis/__version__.py")
    
    if any("missing export" in i for i in issues):
        print("\n3. FIX __init__.py CONTENTS:")
        print("   echo 'from .core import CivilisAgent' > src/civilis/__init__.py")
        print("   echo 'from .simulation import CivilisSimulation' >> src/civilis/__init__.py")
        print("   echo 'from .__version__ import __version__' >> src/civilis/__init__.py")
        print("   echo '__all__ = [\"CivilisAgent\", \"CivilisSimulation\", \"__version__\"]' >> src/civilis/__init__.py")
    
    print("\n4. REINSTALL CORRECTLY:")
    print("   pip uninstall -y civilis")
    print("   pip install -e \".[dev]\"")
    
    print("\n5. VERIFY FIX:")
    print("   python verify_install.py")

def main():
    print("="*50)
    print("CIVILIS INSTALLATION VERIFICATION")
    print("="*50)
    
    # 检查项目结构
    structure_issues = check_project_structure()
    if structure_issues:
        print("🚨 CRITICAL STRUCTURE ISSUES DETECTED:")
        for issue in structure_issues:
            print(issue)
        print_fix_instructions(structure_issues)
        sys.exit(1)
    
    # 检查运行时
    runtime_issues = check_installation()
    if runtime_issues:
        print("🔥 RUNTIME ERRORS DETECTED:")
        for issue in runtime_issues:
            print(issue)
        print_fix_instructions(runtime_issues)
        sys.exit(1)
    
    # 成功
    print("\n" + "="*50)
    print("🎉 PERFECT! ALL SYSTEMS OPERATIONAL")
    print(f"✅ Civilis v{__import__('civilis').__version__} is fully functional")
    print("\n🚀 NEXT STEPS:")
    print("   • Explore examples/colab_demo.ipynb")
    print("   • Run: python examples/civilization_100.py")
    print("   • Contribute: https://github.com/civilis-ai/civilis/issues")
    sys.exit(0)

if __name__ == "__main__":
    main()