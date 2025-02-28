# RapidOCR REST API Service

基于 RapidOCR-ONNXRuntime 封装的轻量级 OCR REST API 服务，提供高效的文本识别能力。

## 📌 项目特性

- 开箱即用的 OCR REST API 服务
- 支持图片自动缩放预处理（最大边限制 1024px）
- 并发请求控制（默认最大 4 线程）
- 完善的错误处理及日志记录
- 支持 Docker 容器化部署
- 自动内存管理优化
- 响应数据标准化（JSON 格式）

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Docker（可选）

### Docker 部署方式


# 构建镜像
```bash
docker build -t rapidocr-api .
```
# 运行容器（默认端口 5001）
```bash
docker run -d -p 5001:5001 --name ocr_api rapidocr-api
```
### 本地安装方式
```bash
# 克隆项目
git clone https://github.com/zclcz/rapidocr-api.git
cd rapidocr-api

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

## 📖 API 使用说明
### 请求端点
POST /ocr

### 请求格式
Content-Type: application/octet-stream
Body: 图片二进制数据
### 示例请求
```bash
curl -X POST --data-binary @"test.jpg" http://localhost:5001/ocr
### 响应示例
成功响应：
```json
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
```
错误响应：
```json
{
  "code": 500,
  "msg": "错误描述信息"
}
```
## 调用示例
### Python
```Python
import requests

url = 'http://localhost:5001/ocr'

# 通过文件路径调用
with open('test.jpg', 'rb') as f:
    response = requests.post(url, data=f)
    print(response.json())

# 通过字节流调用
image_bytes = open('test.jpg', 'rb').read()
response = requests.post(url, data=image_bytes)
print(response.text)
### Java
```java
import java.net.URI;
import java.net.http.*;
import java.nio.file.Path;

public class OCRDemo {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5001/ocr"))
                .header("Content-Type", "application/octet-stream")
                .POST(HttpRequest.BodyPublishers.ofFile(Path.of("test.jpg")))
                .build();

        HttpResponse<String> response = client.send(
                request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```
### Node.js
```JavaScript
const axios = require('axios');
const fs = require('fs');

const url = 'http://localhost:5001/ocr';

// 通过文件流调用
fs.readFile('test.jpg', (err, data) => {
    if (err) throw err;
    
    axios.post(url, data, {
        headers: {
            'Content-Type': 'application/octet-stream'
        }
    })
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
});

// 通过 Buffer 调用（推荐）
const imageBuffer = fs.readFileSync('test.jpg');
axios.post(url, imageBuffer)
    .then(response => console.log(response.data));
```
### Go
```Go
package main

import (
    "bytes"
    "fmt"
    "io"
    "net/http"
    "os"
)

func main() {
    url := "http://localhost:5001/ocr"
    
    // 通过文件读取
    file, _ := os.Open("test.jpg")
    defer file.Close()
    
    resp, err := http.Post(url, "application/octet-stream", file)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
    
    // 通过字节切片调用
    data, _ := os.ReadFile("test.jpg")
    resp, _ = http.Post(url, "application/octet-stream", bytes.NewReader(data))
    // ...处理响应...
}
```
### 响应状态码说明
状态码	说明
100	成功
400	请求参数错误
500	服务端错误或队列已满

## ⚙️ 配置参数
可通过以下方式自定义配置：

### 并发控制

修改 max_workers 值调整最大并发数。

### 图片处理

resize_image() 函数参数：

max_size: 最大边长限制（默认 1024px）
quality: 图片压缩质量（默认 95）
### 服务端口

修改 Dockerfile 或启动命令中的 --port 参数。

## 📝 注意事项
建议图片分辨率不超过 2000x2000px。
单次请求处理时间与图片复杂度正相关。
生产环境建议使用反向代理（如 Nginx）。
日志级别可通过修改 logging.basicConfig 调整。
ONNX 模型文件会自动下载到 ~/.rapidocr 目录。

## 🔍 性能优化
使用 ONNXRuntime 加速推理
自动内存回收机制
图片预处理压缩技术
线程级并发控制
