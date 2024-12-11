import argparse
from . import generate_image_and_save

# 创建解析器
parser = argparse.ArgumentParser(description="Process some parameters.")

# 添加参数
parser.add_argument('-t', '--text'  , type=str, help='Text to display', required=True)
parser.add_argument('-o', '--output', type=str, help='Output filename', required=True)

# 解析参数
args = parser.parse_args().__dict__

# 保存到文件
generate_image_and_save(args["text"], args["output"])