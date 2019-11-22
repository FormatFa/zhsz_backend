from flask import jsonify
def api_result(code,data=None,msg=""):
    return jsonify({
        'code':code,
        'data':data,
        'msg':msg
    })