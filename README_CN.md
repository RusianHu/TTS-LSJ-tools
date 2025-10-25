# TTS Standalone - 独立文本转语音工具

[English](README.md) | 简体中文

这是一个从 [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) 项目中提取的独立TTS（文本转语音）工具，提供简洁的WebUI界面。

## ✨ 功能特性

- 🎙️ **多种TTS引擎支持**
  - Azure TTS V1 (免费，基于Edge TTS)
  - Azure TTS V2 (需要API KEY，音质更好)
  - 硅基流动 (SiliconFlow，需要API KEY)

- 🌍 **多语言支持**
  - 支持中文、英文、日文、韩文等100+种语言
  - 提供丰富的语音选择（男声/女声）

- 📝 **字幕生成**
  - 自动生成SRT格式字幕文件
  - 支持按标点符号智能分句

- 🎨 **友好的WebUI界面**
  - 基于Streamlit构建
  - 简洁直观的操作界面
  - 支持中英文界面切换

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
cd TTS_Standalone
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2️⃣ 测试安装

```bash
python test_installation.py
```

### 3️⃣ 启动WebUI

**Windows:**
```bash
双击 webui.bat
```

**Linux/Mac:**
```bash
chmod +x webui.sh
./webui.sh
```

或直接运行：
```bash
streamlit run webui/Main.py
```

### 4️⃣ 开始使用

浏览器会自动打开 http://localhost:8501

## 📖 详细文档

- [快速入门指南](QUICKSTART.md) - 详细的安装和使用说明
- [README](README.md) - 英文版说明文档

## 🎯 使用示例

### 使用Azure TTS V1（免费）

1. 启动WebUI
2. 选择"Azure TTS V1"
3. 选择语音（如：zh-CN-XiaoxiaoNeural 晓晓-女性）
4. 输入文本
5. 点击"生成语音"

无需任何配置，即可使用！

### 使用Azure TTS V2（更高音质）

1. 获取Azure Speech API密钥：
   - 访问 [Azure Portal](https://portal.azure.com)
   - 创建"语音服务"资源
   - 获取密钥和区域

2. 编辑 `config.toml`：
   ```toml
   [azure]
   speech_key = "你的密钥"
   speech_region = "eastasia"
   ```

3. 在WebUI中选择"Azure TTS V2"

### 使用硅基流动

1. 获取API密钥：
   - 访问 [SiliconFlow](https://siliconflow.cn)
   - 注册并获取API密钥

2. 编辑 `config.toml`：
   ```toml
   [siliconflow]
   api_key = "你的密钥"
   ```

3. 在WebUI中选择"SiliconFlow"

## 📁 项目结构

```
TTS_Standalone/
├── app/
│   ├── config/          # 配置管理
│   ├── services/        # TTS服务
│   │   └── voice.py     # 核心TTS实现
│   └── utils/           # 工具函数
├── webui/
│   ├── i18n/            # 国际化
│   │   ├── zh.json      # 中文
│   │   └── en.json      # 英文
│   └── Main.py          # WebUI主程序
├── storage/
│   ├── temp/            # 临时文件
│   └── output/          # 输出文件
├── config.toml          # 配置文件
├── requirements.txt     # 依赖列表
├── test_installation.py # 安装测试
├── webui.bat            # Windows启动脚本
├── webui.sh             # Linux/Mac启动脚本
├── README.md            # 英文说明
├── README_CN.md         # 中文说明
└── QUICKSTART.md        # 快速入门
```

## 🎤 推荐语音

### 中文

**免费版 (Azure TTS V1):**
- 女声：zh-CN-XiaoxiaoNeural（晓晓）⭐ 推荐
- 女声：zh-CN-XiaoyiNeural（晓伊）
- 男声：zh-CN-YunxiNeural（云希）⭐ 推荐
- 男声：zh-CN-YunyangNeural（云扬）

**高级版 (Azure TTS V2):**
- 女声：zh-CN-XiaoxiaoMultilingualNeural-V2 ⭐⭐ 强烈推荐
- 男声：zh-CN-YunxiMultilingualNeural-V2 ⭐⭐ 强烈推荐

### 英文

**免费版 (Azure TTS V1):**
- 女声：en-US-JennyNeural ⭐ 推荐
- 女声：en-US-AriaNeural
- 男声：en-US-GuyNeural ⭐ 推荐
- 男声：en-US-ChristopherNeural

**高级版 (Azure TTS V2):**
- 女声：en-US-AvaMultilingualNeural-V2 ⭐⭐ 强烈推荐
- 男声：en-US-AndrewMultilingualNeural-V2 ⭐⭐ 强烈推荐

## ❓ 常见问题

### 安装依赖失败？

使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Azure TTS V2无法使用？

检查：
- ✅ 是否正确配置了 `speech_key` 和 `speech_region`
- ✅ API密钥是否有效
- ✅ 网络连接是否正常

### 生成的音频没有声音？

检查：
- ✅ 语音语言是否与文本匹配（中文文本选中文语音）
- ✅ 尝试更换其他语音
- ✅ 检查网络连接

### 字幕文件乱码？

使用支持UTF-8编码的文本编辑器打开SRT文件。

## 🛠️ 技术栈

- **Python 3.10+**
- **Streamlit** - WebUI框架
- **edge-tts** - Azure TTS V1实现
- **azure-cognitiveservices-speech** - Azure TTS V2 SDK
- **moviepy** - 音频处理
- **loguru** - 日志管理

## 📄 许可证

本项目基于 [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) 项目提取，遵循原项目的开源许可证。

## 🙏 致谢

感谢 [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) 项目提供的优秀TTS实现。

## 📝 更新日志

### v1.0.0 (2025-10-25)
- ✨ 初始版本发布
- ✨ 支持Azure TTS V1、V2和硅基流动
- ✨ 提供WebUI界面
- ✨ 支持字幕生成
- ✨ 支持中英文界面

## 💡 使用技巧

1. **批量生成**：可以多次点击"生成语音"，每次都会生成新的文件
2. **试听功能**：使用"试听声音"按钮可以快速测试不同的语音效果
3. **字幕编辑**：生成的SRT字幕文件可以用任何文本编辑器编辑
4. **语音选择**：建议先用免费的Azure TTS V1测试，满意后再考虑使用V2

## 🔗 相关链接

- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - 原项目
- [Azure Speech Service](https://azure.microsoft.com/zh-cn/services/cognitive-services/speech-services/) - Azure语音服务
- [SiliconFlow](https://siliconflow.cn) - 硅基流动
- [Streamlit](https://streamlit.io/) - WebUI框架

---

如有问题或建议，欢迎提Issue！ 🎉

