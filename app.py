# -*- coding: utf-8 -*-
from rapidocr_onnxruntime import RapidOCR
from flask import Flask, request, jsonify
import logging
import json
from PIL import Image
import io
import numpy as np  # 新增 numpy 支持
import threading
import time

app = Flask(__name__)
ocr = RapidOCR()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s [%(threadName)s] - %(message)s')

max_workers = 4  # 最大并发工作线程数
semaphore = threading.Semaphore(max_workers)  # 创建信号量


def resize_image(image_stream, max_size=1024):
    """调整图像大小（保持宽高比，限制最大边长）"""
    image = Image.open(image_stream)
    width, height = image.size
    logging.info(f"原始图片尺寸：宽度={width}, 高度={height}")

    # 转换为 RGB 模式（避免 Alpha 通道问题）
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 如果需要缩放，则打印消息
    if width > max_size or height > max_size:
        logging.info(f"开始缩放图片以适应最大尺寸 {max_size}x{max_size}")

    # 如果原图的长和宽都小于等于1024，则不进行缩放
    if width <= max_size and height <= max_size:
        with io.BytesIO() as img_byte_arr:
            image.save(img_byte_arr, format='JPEG', quality=95)  # 直接保存原图
            return img_byte_arr.getvalue()
    else:
        # 按比例缩放
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))

        image_resized = image.resize(new_size, Image.LANCZOS)
        with io.BytesIO() as img_byte_arr:
            image_resized.save(img_byte_arr, format='JPEG', quality=95)  # 使用 JPEG 减少内存占用
            return img_byte_arr.getvalue()

def extract_text_with_rapidocr(image_bytes):
    """使用 RapidOCR-ONNXRuntime 提取图片文本"""
    try:
        resized_image_data = resize_image(io.BytesIO(image_bytes))
        img_np = np.array(Image.open(io.BytesIO(resized_image_data)))
        result, elapse = ocr(img_np)
        del img_np  # 手动删除大数组以提示垃圾回收
        logging.info(f"OCR 返回的原始结果：{result}")

        formatted_data = []
        if result:
            for item in result:
                try:
                    if len(item) == 3:
                        box = item[0]
                        text = item[1]
                        score = float(item[2])
                        formatted_data.append({"box": box, "text": text, "score": score})
                except Exception as e:
                    logging.warning(f"跳过无效数据项：{str(e)}")
                    continue

        if not formatted_data:
            return {"code": 500, "msg": "图片内没有文本内容"}

        return {"code": 100, "data": formatted_data}

    except Exception as e:
        logging.exception("OCR Error:")
        return {"code": 500, "msg": f"OCR Error: {str(e)}"}


@app.route('/ocr', methods=['POST'])
def ocr_api():
    # 尝试获取信号量，如果无法获取则意味着已经达到最大并发数
    if not semaphore.acquire(blocking=False):
        logging.warning("拒绝新请求：已达最大并发处理数。")
        return jsonify({"code": 500, "msg": "服务当前运行的任务过多，请稍后再试"}), 500

    start_time = time.time()  # 记录开始时间
    current_thread_name = threading.current_thread().getName()  # 获取当前线程名称

    try:
        # 直接从请求体中读取二进制数据
        file_bytes = request.get_data()

        if not file_bytes:
            logging.error(f"[{current_thread_name}] 请求中缺少文件数据")
            return jsonify({"code": 400, "msg": "No data part"}), 400

        result = extract_text_with_rapidocr(file_bytes)
        logging.info(f"[{current_thread_name}] 成功处理请求，结果：{result}")

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算总耗时
        logging.info(f"[{current_thread_name}] 接口任务总耗时：{elapsed_time:.2f}秒")

        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.exception(f"[{current_thread_name}] API 处理过程中发生错误:")
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        # 确保释放信号量，无论处理过程中是否发生异常
        logging.info(f"[{current_thread_name}] 释放信号量")
        semaphore.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3746)