import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import path
import pandas as pd
# 导入配置，用于找app位置
import myconfig
# 导入Controller们
from controller.DataProcess import Interpolation
# 生成随机字符串
import exrex
import time

# 注册APP
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# 注册跨域
CORS(app, resources=r'/*')  # 注册CORS, "/*" 允许访问所有api

# 蓝图。注册其他的controller接口
# 注册插值API
app.register_blueprint(Interpolation.app, url_prefix='/interpolation')
# 注册配置项的API
app.register_blueprint(myconfig.app, url_prefix='/')

# 统一上传文件
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    # 后缀
    suffix = f.filename.split(".")[-1]
    # 随机生成文件名
    filename = time.strftime('%Y%m%d%H%M%S', time.localtime()) + exrex.getone(r'[a-zA-Z0-9]{10}') + "." + suffix
    # 文件要存放的目标位置
    upload_path = path.join(path.dirname(path.abspath(sys.argv[0])), myconfig.input_path, filename)
    print("文件存放的目标位置", upload_path)

    try:
        f.save(upload_path)
        return jsonify(upload_path)
    except Exception as e:
        print(e)
        return jsonify(0)


# 将Excel文件返回JSON给前端
@app.route('/selectAllByExcel', methods=['POST'])
def selectAllByExcel():
    # 获取前端参数
    data = request.get_json()
    filename = data['fileName']
    # 后缀
    suffix = filename.split(".")[-1]
    if suffix == ".xls" or suffix == ".xlsx":
        input_path = path.join(path.dirname(path.abspath(sys.argv[0])), myconfig.input_path, filename)
        # 读取数据
        df = pd.read_excel(input_path)
        return jsonify(df.to_dict(orient='records'))
    return jsonify(0)

def initWorkSpace():
    print("---初始化工作空间---")
    for p in myconfig.init_paths:
        # 这里有一个坑，所有路径拼接都应该统一使用path.join
        pth = path.join(path.dirname(path.abspath(sys.argv[0])), p)
        if not path.isdir(pth):  # 如果不是一个已经存在的目录，创建目录
            print(f"{pth}不存在,开始初始化")
            try:
                os.makedirs(pth)
                print(f"成功创建目录{pth}")

            except Exception as e:
                print(f"创建目录{pth}失败", e)


if __name__ == '__main__':
    initWorkSpace()
    app.run(host='127.0.0.1', port=12138)
