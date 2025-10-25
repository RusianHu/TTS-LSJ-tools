# 快速入门指南

## 一、安装

### 1. 进入项目目录

```bash
cd TTS_Standalone
```

### 2. 安装Python依赖

使用国内镜像源加速安装：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 二、配置（可选）

如果只使用Azure TTS V1（免费版），无需配置，可直接跳到第三步。

如果要使用Azure TTS V2或硅基流动，需要配置API密钥：

1. 复制配置文件（首次运行会自动创建）：
   ```bash
   copy config.example.toml config.toml  # Windows
   cp config.example.toml config.toml    # Linux/Mac
   ```

2. 编辑 `config.toml` 文件，填入API密钥：

   **Azure TTS V2配置：**
   ```toml
   [azure]
   speech_key = "你的Azure Speech API Key"
   speech_region = "eastasia"  # 或其他区域
   ```

   **硅基流动配置：**
   ```toml
   [siliconflow]
   api_key = "你的SiliconFlow API Key"
   ```

### API密钥获取方式

- **Azure Speech API**: 
  1. 访问 https://portal.azure.com
  2. 创建"语音服务"资源
  3. 在"密钥和终结点"中获取密钥和区域

- **SiliconFlow API**: 
  1. 访问 https://siliconflow.cn
  2. 注册账号
  3. 在控制台获取API密钥

## 三、启动

### Windows用户

双击运行 `webui.bat` 文件

或在命令行中执行：
```bash
streamlit run webui/Main.py
```

### Linux/Mac用户

```bash
chmod +x webui.sh
./webui.sh
```

或直接运行：
```bash
streamlit run webui/Main.py
```

## 四、使用

1. 浏览器会自动打开 http://localhost:8501

2. 在界面中：
   - 选择TTS服务器（推荐先用Azure TTS V1免费版）
   - 选择语音（如：zh-CN-XiaoxiaoNeural 晓晓-女性）
   - 调整语音参数（音量、速度）
   - 输入要转换的文本
   - 点击"生成语音"

3. 生成完成后：
   - 可以在线播放
   - 下载音频文件（MP3格式）
   - 下载字幕文件（SRT格式）

## 五、常见问题

### 1. 安装依赖失败

**问题**：pip安装速度慢或失败

**解决**：使用国内镜像源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 启动失败

**问题**：提示找不到streamlit

**解决**：确保已安装依赖
```bash
pip install streamlit
```

### 3. Azure TTS V1可以用，但V2不行

**问题**：提示需要API Key

**解决**：
- 确保已在config.toml中配置speech_key和speech_region
- 检查API密钥是否正确
- 确认Azure账户有足够的配额

### 4. 生成的音频没有声音

**问题**：音频文件生成了但播放无声

**解决**：
- 检查选择的语音是否与文本语言匹配（如中文文本要选中文语音）
- 尝试更换其他语音
- 检查网络连接

### 5. 字幕文件乱码

**问题**：SRT字幕文件打开乱码

**解决**：使用支持UTF-8编码的文本编辑器打开

## 六、推荐配置

### 中文语音推荐

**Azure TTS V1（免费）：**
- 女声：zh-CN-XiaoxiaoNeural（晓晓）
- 女声：zh-CN-XiaoyiNeural（晓伊）
- 男声：zh-CN-YunxiNeural（云希）
- 男声：zh-CN-YunyangNeural（云扬）

**Azure TTS V2（需要API Key，音质更好）：**
- 女声：zh-CN-XiaoxiaoMultilingualNeural-V2
- 男声：zh-CN-YunxiMultilingualNeural-V2

### 英文语音推荐

**Azure TTS V1（免费）：**
- 女声：en-US-JennyNeural
- 女声：en-US-AriaNeural
- 男声：en-US-GuyNeural
- 男声：en-US-ChristopherNeural

**Azure TTS V2（需要API Key）：**
- 女声：en-US-AvaMultilingualNeural-V2
- 女声：en-US-EmmaMultilingualNeural-V2
- 男声：en-US-AndrewMultilingualNeural-V2
- 男声：en-US-BrianMultilingualNeural-V2

### 参数建议

- **语音音量**：1.0（100%）
- **语音速度**：
  - 正常语速：1.0
  - 稍快：1.2
  - 较快：1.5
  - 慢速：0.8

## 七、输出文件位置

生成的文件保存在：
- 音频文件：`storage/output/tts-xxxxx.mp3`
- 字幕文件：`storage/output/tts-xxxxx.srt`

临时文件保存在：
- `storage/temp/`

## 八、技巧

1. **批量生成**：可以多次点击"生成语音"，每次都会生成新的文件
2. **试听功能**：使用"试听声音"按钮可以快速测试不同的语音效果
3. **字幕编辑**：生成的SRT字幕文件可以用任何文本编辑器编辑
4. **语音选择**：建议先用免费的Azure TTS V1测试，满意后再考虑使用V2

## 九、下一步

- 尝试不同的语音和参数组合
- 使用生成的音频制作视频
- 将字幕文件导入视频编辑软件

祝使用愉快！🎉

