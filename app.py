import os
import random
from flask import Flask, request, send_file, render_template
from utils import find_avatar
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB

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
        find_avatar(random_str)
    except Exception as e:
        print(f"find_avatar error: {e}")
        return {'error': str(e)}, 500

    # 获取输出图片路径
    output_path = f'output/{random_str}.jpg'

    if not os.path.exists(output_path):
        return {'error': 'Processing failed'}, 500

    print(f"output_path: {output_path}")
    # 返回处理后的图片
    return send_file(output_path, mimetype='image/jpeg')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
