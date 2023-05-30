import sys
from os import path
from flask import Blueprint

# 注册
app = Blueprint('myconfig', __name__)

# 用来存储各种数据和配置文件
input_path = "run\\input"
output_path = "run\\output"

init_paths = [input_path, output_path]

sys_path = path.dirname(path.abspath(sys.argv[0]))

# 这里有个坑，世界import之后 sys_path 获取的不是myconfig文件中的路径，而是import进入的文件的路径
@app.route('/syspath', methods=['GET'])
def getSysPath():
    return sys_path


if __name__ == '__main__':
    print(path.dirname(path.abspath(sys.argv[0])))
