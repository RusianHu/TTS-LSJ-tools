# TTS-LSJ-Tools - 独立文本转语音工具

简易的 TTS（文本转语音）工具，基于 Streamlit 构建简洁的 WebUI 界面。

## 功能特性

- 🎙️ **TTS引擎支持**
  - Azure TTS V1 (免费，基于Edge TTS)
  - Azure TTS V2 (需要API KEY，音质更好)
  - 硅基流动 (SiliconFlow，需要API KEY)

- 📝 **字幕生成**
  - 自动生成SRT格式字幕文件
  - 支持按标点符号智能分句

## 安装步骤

### 1. 克隆或下载项目

```bash
cd TTS-LSJ-Tools
```

### 2. 安装依赖

建议使用Python 3.10或更高版本。

```bash
pip install -r requirements.txt
```

### 3. 配置文件

首次运行时，程序会自动从 `config.example.toml` 复制生成 `config.toml` 配置文件。

如果需要使用Azure TTS V2或硅基流动，请编辑 `config.toml` 文件，填入相应的API密钥：

```toml
[azure]
# Azure Speech API Key
speech_key = "your_azure_speech_key"
speech_region = "your_region"  # 例如: eastasia, westus

[siliconflow]
# SiliconFlow API Key
api_key = "your_siliconflow_api_key"
```

#### 获取API密钥

- **Azure Speech API**: 访问 [Azure Portal](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices) 获取
- **SiliconFlow API**: 访问 [SiliconFlow官网](https://siliconflow.cn) 注册获取

## 使用方法

### 启动WebUI

#### Windows

双击运行 `webui.bat` 或在命令行中执行：

```bash
streamlit run webui/Main.py
```

#### Linux/Mac

```bash
chmod +x webui.sh
./webui.sh
```

或直接运行：

```bash
streamlit run webui/Main.py
```

### 使用界面

1. **选择TTS服务器**：根据需要选择Azure TTS V1、V2或硅基流动
2. **选择语音**：从下拉列表中选择合适的语音
3. **配置参数**：
   - 如使用Azure TTS V2，需填写Speech Region和API Key
   - 如使用硅基流动，需填写API Key
   - 调整语音音量和速度
4. **输入文本**：在文本框中输入要转换的文本
5. **生成语音**：
   - 点击"试听声音"按钮可以快速试听
   - 点击"生成语音"按钮生成完整的音频和字幕文件
6. **下载文件**：生成完成后可以下载音频和字幕文件

## 目录结构

```
TTS-LSJ-Tools/
├── app/
│   ├── config/          # 配置管理模块
│   ├── services/        # TTS服务模块
│   └── utils/           # 工具函数
├── webui/
│   ├── i18n/            # 国际化文件
│   └── Main.py          # WebUI主程序
├── storage/
│   ├── temp/            # 临时文件
│   └── output/          # 输出文件
├── config.toml          # 配置文件（首次运行自动生成）
├── config.example.toml  # 配置文件示例
├── requirements.txt     # Python依赖
├── webui.bat            # Windows启动脚本
├── webui.sh             # Linux/Mac启动脚本
└── README.md            # 项目说明
```

## 支持的语音

### Azure TTS V1 (免费)
- 支持100+种语言和方言
- 包含中文、英文、日文、韩文等常用语言
- 男声和女声可选

### Azure TTS V2 (需要API KEY)
- 更高质量的语音合成
- 支持多语言神经网络语音
- 更自然的语音表现

### 硅基流动 (需要API KEY)
- 基于CosyVoice2模型
- 支持多种音色
- 可调节语速和音量

## 技术栈

- **Python 3.10+**
- **Streamlit**: WebUI框架
- **edge-tts**: Azure TTS V1实现
- **azure-cognitiveservices-speech**: Azure TTS V2 SDK
- **moviepy**: 音频处理
- **loguru**: 日志管理