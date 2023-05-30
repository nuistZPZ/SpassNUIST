from flask import Blueprint, request, jsonify
from service.DataProcess import Interpolation
import myconfig

# 注册插值功能
app = Blueprint('Interpolation', __name__)


@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()

    # 用户选择数据，算法名，新的点的生成 起点、重点、数量
    fileName = data['fileName']
    kind = data['kind']  # kind  ['zero', 'slinear', 'quadratic', 'cubic']
    start = data['start']
    end = data['end']
    num = data['num']
    x_colName = data['x_colName']
    y_colName = data['y_colName']

    print(y_colName)

    data, url = Interpolation.interp1d(kind=kind, start=start,end=end,num=num,fileName=fileName,x_colName=x_colName,y_colName=y_colName)

    result={"data":data.to_dict(orient='records'),"url":url}

    print(result)

    return jsonify(result)
