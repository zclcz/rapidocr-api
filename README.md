# RapidOCR REST API Service

基于RapidOCR-ONNXRuntime封装的轻量级OCR REST API服务，提供高效的文本识别能力。

## 📌 项目特性

- **开箱即用**：提供即时可用的OCR REST API服务。
- **自动缩放**：支持图片自动缩放预处理（最大边限制1024px）。
- **并发控制**：默认最大4线程的并发请求控制。
- **错误处理与日志记录**：完善的错误处理机制及详细的日志记录。
- **容器化部署**：支持Docker容器化部署，便于快速上线。
- **内存管理**：自动化的内存管理优化。
- **标准化响应**：所有响应数据均以JSON格式返回。

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Docker（若选择使用）

### 部署指南

#### 使用Docker部署

# 构建镜像
docker build -t rapidocr-api .

# 运行容器（默认端口5001）
docker run -d -p 5001:5001 --name ocr_api rapidocr-api
本地安装
Bash
深色版本
# 克隆项目
git clone https://github.com/zclcz/rapidocr-api.git
cd rapidocr-api

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
📖 API使用说明

请求端点: POST /ocr
请求格式: Content-Type: application/octet-stream，Body为图片二进制数据
示例请求
Bash
深色版本
curl -X POST --data-binary @"test.jpg" http://localhost:5001/ocr
响应示例
成功响应

Json
深色版本
{
  "code": 100,
  "data": [
    {
      "box": [[10,20], [30,20], [30,40], [10,40]],
      "text": "识别文本",
      "score": 0.98
    }
  ]
}
错误响应

Json
深色版本
{
  "code": 500,
  "msg": "错误描述信息"
}
多语言调用示例
包括Python、Java、Node.js、Go等语言的调用实例，请参考此处。

⚙️ 配置参数

并发控制：通过修改max_workers值来调整最大并发数。
图片处理：resize_image()函数参数允许设置最大边长和压缩质量。
服务端口：可以通过修改Dockerfile或启动命令中的--port参数来指定。
📝 注意事项

建议图片分辨率不超过2000x2000px。
请求处理时间取决于图片复杂度。
生产环境中建议使用反向代理如Nginx。
日志级别可通过修改logging.basicConfig进行调整。
🔍 性能优化

使用ONNXRuntime加速推理过程。
实现了自动内存回收机制。
应用了图片预处理压缩技术。
提供了线程级并发控制。
📜 许可证

本项目遵循MIT License。

使用说明：

将上述内容复制到项目的README.md文件中。
确保LICENSE文件位于项目根目录。
准备一个test.jpg作为示例图片。
根据实际需求调整配置参数。
深色版本

此版本进行了以下优化：
- 使用标题和列表增强结构清晰度。
- 调整代码块和示例请求格式，使其更易于阅读。
- 清晰地分隔不同部分的内容，以便于用户快速找到所需信息。
