#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TTS Standalone 安装测试脚本
用于验证项目是否正确安装和配置
"""

import sys
import os

# 添加项目根目录到系统路径
root_dir = os.path.dirname(os.path.realpath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

def test_imports():
    """测试必要的模块是否可以导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    modules = [
        ("streamlit", "Streamlit"),
        ("edge_tts", "Edge TTS"),
        ("loguru", "Loguru"),
        ("requests", "Requests"),
        ("toml", "TOML"),
        ("moviepy", "MoviePy"),
    ]
    
    failed = []
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {display_name:20s} - 已安装")
        except ImportError as e:
            print(f"✗ {display_name:20s} - 未安装")
            failed.append(module_name)
    
    # 测试Azure Speech SDK（可选）
    try:
        import azure.cognitiveservices.speech
        print(f"✓ {'Azure Speech SDK':20s} - 已安装")
    except ImportError:
        print(f"○ {'Azure Speech SDK':20s} - 未安装（可选，仅Azure TTS V2需要）")
    
    print()
    
    if failed:
        print("❌ 以下模块未安装，请运行以下命令安装：")
        print(f"   pip install {' '.join(failed)}")
        return False
    else:
        print("✅ 所有必需模块已安装")
        return True


def test_project_structure():
    """测试项目结构是否完整"""
    print("=" * 60)
    print("测试项目结构...")
    print("=" * 60)
    
    required_paths = [
        ("app", "目录"),
        ("app/config", "目录"),
        ("app/services", "目录"),
        ("app/utils", "目录"),
        ("webui", "目录"),
        ("webui/i18n", "目录"),
        ("storage", "目录"),
        ("storage/temp", "目录"),
        ("storage/output", "目录"),
        ("config.example.toml", "文件"),
        ("requirements.txt", "文件"),
        ("webui/Main.py", "文件"),
        ("app/services/voice.py", "文件"),
    ]
    
    missing = []
    for path, path_type in required_paths:
        full_path = os.path.join(root_dir, path)
        if os.path.exists(full_path):
            print(f"✓ {path:30s} - 存在")
        else:
            print(f"✗ {path:30s} - 缺失")
            missing.append(path)
    
    print()
    
    if missing:
        print("❌ 以下文件或目录缺失：")
        for path in missing:
            print(f"   - {path}")
        return False
    else:
        print("✅ 项目结构完整")
        return True


def test_config():
    """测试配置文件"""
    print("=" * 60)
    print("测试配置...")
    print("=" * 60)
    
    try:
        from app.config import config
        print(f"✓ 配置文件加载成功")
        print(f"  - 项目名称: {config.project_name}")
        print(f"  - 项目版本: {config.project_version}")
        print(f"  - 日志级别: {config.log_level}")
        
        # 检查配置项
        if hasattr(config, 'azure'):
            print(f"  - Azure配置: 已加载")
        if hasattr(config, 'siliconflow'):
            print(f"  - SiliconFlow配置: 已加载")
        if hasattr(config, 'ui'):
            print(f"  - UI配置: 已加载")
        
        print()
        print("✅ 配置加载成功")
        return True
    except Exception as e:
        print(f"✗ 配置加载失败: {str(e)}")
        print()
        print("❌ 配置加载失败")
        return False


def test_voice_module():
    """测试语音模块"""
    print("=" * 60)
    print("测试语音模块...")
    print("=" * 60)
    
    try:
        from app.services import voice
        
        # 测试获取语音列表
        azure_voices = voice.get_all_azure_voices(filter_locals=["zh-CN", "en-US"])
        print(f"✓ Azure语音列表获取成功 (共 {len(azure_voices)} 个)")
        
        siliconflow_voices = voice.get_siliconflow_voices()
        print(f"✓ SiliconFlow语音列表获取成功 (共 {len(siliconflow_voices)} 个)")
        
        # 测试辅助函数
        test_voice = "zh-CN-XiaoxiaoNeural-Female"
        parsed = voice.parse_voice_name(test_voice)
        print(f"✓ 语音名称解析: {test_voice} -> {parsed}")
        
        print()
        print("✅ 语音模块测试通过")
        return True
    except Exception as e:
        print(f"✗ 语音模块测试失败: {str(e)}")
        print()
        print("❌ 语音模块测试失败")
        return False


def test_i18n():
    """测试国际化"""
    print("=" * 60)
    print("测试国际化...")
    print("=" * 60)
    
    try:
        from app.utils import utils
        i18n_dir = os.path.join(root_dir, "webui", "i18n")
        locales = utils.load_locales(i18n_dir)
        
        print(f"✓ 加载了 {len(locales)} 种语言:")
        for code, locale_data in locales.items():
            lang_name = locale_data.get("Language", "Unknown")
            print(f"  - {code}: {lang_name}")
        
        print()
        print("✅ 国际化测试通过")
        return True
    except Exception as e:
        print(f"✗ 国际化测试失败: {str(e)}")
        print()
        print("❌ 国际化测试失败")
        return False


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "TTS Standalone 安装测试" + " " * 19 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_imports()))
    results.append(("项目结构", test_project_structure()))
    results.append(("配置加载", test_config()))
    results.append(("语音模块", test_voice_module()))
    results.append(("国际化", test_i18n()))
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15s}: {status}")
    
    print()
    print(f"总计: {passed}/{total} 项测试通过")
    print()
    
    if passed == total:
        print("🎉 恭喜！所有测试通过，可以开始使用了！")
        print()
        print("运行以下命令启动WebUI：")
        print("  streamlit run webui/Main.py")
        print()
        print("或者：")
        print("  Windows: 双击 webui.bat")
        print("  Linux/Mac: ./webui.sh")
        return 0
    else:
        print("⚠️  部分测试失败，请检查上述错误信息并修复")
        print()
        print("如需帮助，请查看 README.md 或 QUICKSTART.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())

