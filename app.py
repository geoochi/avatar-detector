import os
import random
from flask import Flask, request, send_file
from utils import find_avatar
from pathlib import Path

app = Flask(__name__)

# 确保输入输出目录存在
Path("input").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)


@app.route('/detect_avatar', methods=['POST'])
def detect_avatar():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400

    file = request.files['image']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # 生成随机数并保存上传的图片
    random_str = str(random.random())
    input_path = f'input/{random_str}.jpg'
    file.save(input_path)

    try:
        # 处理图片
        find_avatar(random_str)

        # 获取输出图片路径
        output_path = f'output/{random_str}.jpg'

        if not os.path.exists(output_path):
            return {'error': 'Processing failed'}, 500

        # 返回处理后的图片
        return send_file(output_path, mimetype='image/jpeg')

    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
