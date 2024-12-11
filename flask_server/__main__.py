from flask import Flask, send_file
import argparse
import subprocess
import string
import random
import os
import hashlib

# 项目根目录
dirnow = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(dirnow)

# 创建 image 日志目录
def create_image_log():
    imgdir = os.path.join(dirnow, "image_log")
    os.makedirs(imgdir, exist_ok=True)

# 创建解析器
parser = argparse.ArgumentParser(description="A simple command line parser.")
parser.add_argument('-p', '--port', type=int, help='Specify the port number', required=True)
args = parser.parse_args()

app = Flask(__name__)

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # 包含字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def get_rand_image_path(text: str) -> str:
    create_image_log()
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    return os.path.join(dirnow, "image_log", md5.hexdigest() + ".png")

@app.route('/<path:path>')
def get_pic(path: str):
    rand_image_path = get_rand_image_path(path)
    subprocess.run(["python3", "-m", "i_drop_out_generator", "-t", path, "-o", rand_image_path])
    return send_file(rand_image_path, mimetype='image/jpeg')

@app.route('/')
def main():
    return get_pic("URL：/文字内容[R,G,B]")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=args.port)