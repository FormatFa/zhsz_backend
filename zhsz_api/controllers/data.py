import os
import time

import pandas as pd
from flask import Blueprint, jsonify, request
from flask_login import login_required
from settings import config, FileConfig
from zhsz_api.models import Bigtable,db
from utils.api import api_result
from . import api_blue

ALLOWED_EXTENSIONS = ['xls', 'xlsx', 'csv','jpg','png']


CURRENT =   os.path.dirname(os.path.dirname(__file__))

# 增加目录后面加多一个 /
UPLOAD_PATH = CURRENT + '/uploads/static/'
UPDATA_PATH = CURRENT + '/uploads/updata/'

#建立数据目录
if not os.path.exists(UPLOAD_PATH):
    print("新建上传文件目录:",UPLOAD_PATH,os.makedirs(UPLOAD_PATH))
if not os.path.exists(UPDATA_PATH):
    print("新建解析数据临时目录:",UPDATA_PATH,os.makedirs(UPDATA_PATH))
    

need_word = FileConfig.need_word
key = FileConfig.key
need_columns = FileConfig.need_columns
engine=config.engine

print(engine)

# 允许的名字
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 上传文件--保存在uploads的static/上

# 上传文件--保存在uploads的static/上
'''

'''
@api_blue.route('/data/upload', methods=['POST'])
# @login_required
def upload_file():
    if request.method == 'POST':
        formdata = request.form
        # 检查file参数是否存在,前端请求url ： requests.post('http://127.0.0.1:5000/api_blue/upload', files=files)
        if 'file' not in request.files:
            return api_result(-1,msg="没有上传文件")

        file = request.files['file']
   
        # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空零件
        if file.filename == '':
            return api_result(-1,msg="没有上传文件,文件名为空")
        else:
            try:
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    filename = origin_file_name
                    #加多一个学院
                    uploadfile,datafile=getuploadpath(formdata)
        
                    print(filename, "保存到:",uploadfile)
                    # 文件保存路径以及文件名
                    file.save(uploadfile)

                    return api_result(0,msg="上传成功:"+origin_file_name)
                else:
                    return api_result(-1,msg="不允许上传的文件类型")

            except Exception as e:
                print(e)
                return api_result(-1,msg="上传文件异常:"+str(e))
    else:
        return api_result(-1,msg="不允许非POST方法请求")



STATUS_NOUPLOAD = 0
STATUS_NOPARSE = 1
STATUS_DONE = 2
states = {
    0: "未上传",
    1: "未解析",
    2: "解析完成"
}

# 获取文件状态
def getstate(college, year, grade, term):

    up_path,data_path = getuploadpath({"college":college,"year":year,"grade":grade,"term":term})

    print('判断状态:', up_path, data_path)
    code = STATUS_NOUPLOAD
    if not os.path.exists(up_path):
        code = STATUS_NOUPLOAD
    if os.path.exists(up_path) and not os.path.exists(data_path):
        code = STATUS_NOPARSE
    if os.path.exists(data_path):
        code = STATUS_DONE

    return code

def getuploadpath(formdata):
    uploadfile ="{}-{}-{}-{}.xls".format(formdata['college'], formdata['year'], formdata['grade'], formdata['term'])
    datafile = "{}-{}-{}-{}.csv".format(formdata['college'],formdata['year'], formdata['grade'], formdata['term'])
    return os.path.join(UPLOAD_PATH ,uploadfile), os.path.join(UPDATA_PATH, datafile)

# 处理文件--将处理好的文件保存到uploads的updata/上
@api_blue.route('/data/handle', methods=['POST'])
def handle_file():
    if request.method == 'POST':
        formdata = request.json

        up_path,data_path = getuploadpath(formdata)

        try:

            save_csv = data_path.replace('.xls', '.csv')  # 保存的路径
            print("解析数据的路径:", up_path, save_csv)

            excel = pd.ExcelFile(up_path)
            big_data_name = excel.sheet_names  # 拿到所有的sheetname
            print(big_data_name)
            for needs in need_columns:  # 循环所有可能出现的表头
                # 增加多两列数据
                print(needs)
                for i in big_data_name:  # 循环所有的sheetname
                    data = pd.read_excel(up_path, sheet_name=i, header=2,converters={u'学号':str})

                    headers = data.columns.tolist()  # 将表头转换成列表的形式

                    if headers == needs:  # 将可能出现的表头与excel里面的header对应
                        data = data.drop(columns=['排名'])  # 删除排名
                        # data['年级'] = re.findall('\w+级', filenames)[0]
                        # data['学期'] = re.findall('.*?(第.*?期).*?', filenames)[0]
                        data['年级'] = formdata['grade']
                        if formdata['term']=="term1":
                            term="第一学期"
                        elif formdata['term']=="term2":
                            term="第二学期"
                        data['学期'] = term
                        data['年度']=  formdata['year']
                        data['学院']=formdata['college']

                        head = data.columns.tolist()
                        app = []
                        

                        for k in range(0, len(key)):  # 替换表头的名字 -- 将中文的表头变成英文的表头，固定死
                            if head[k] == key[k]:
                                pass
                            else:
                                head[k] = key[k]
                        for h in head:
                            app.append(need_word[h])
                        data.columns = app
                        data.to_csv(save_csv, encoding='utf-8', index=False)

                        # 需要改数据库和数据表
                        print("成功保存为csv文件")
                        time.sleep(3)
                        try:
                            data.to_sql("zhsz", con=engine, if_exists='append', index=False)
                            print("导入数据库成功")
                        except:
                            print()

            # 修改上传数据库代码
            return api_result(0,msg="导入数据到mysql成功!")


        except Exception as e:
            return api_result(-1,msg="导入数据到mysql失败!"+str(e))

    else:
        return api_result(0,msg="Metho not allow")


@api_blue.route('/data/truncate', methods=['POST'])
@login_required
def truncate():
    # 清空表
    print("正在清空表...")

    return "ok"

# uploaded
@api_blue.route("/data/uploaded",methods=['POST'])
@login_required
def uploaded():
    result = get_upload_data()
    return api_result(0,data=result)
# 扫描上传的目录，获取上传的文件信息
def get_upload_data():
    files = os.listdir(UPLOAD_PATH)
    # file 
    result = []
    for file in files:
        if not file.endswith(".xls"):
            continue
        name = file.replace(".xls",'')
        college,year,grade,term = name.split("-")
        result.append({
            'college':college,
            'year':year,
            'grade':grade,
            'term':term,
            'state':getstate(college, year,grade,term)
        })
    return result

# 判断文件在不在
# @api_blue.route('/data/files', methods=['POST'])
# def files():
#     json = request.json
#     year = int(json['year'])

#     files = []
#     for i in range(year - 2, year + 1):
#         state = getstate(year, i, "term1")
#         files.append({
#             'year': year,
#             'grade': str(i),
#             'college': "大数据与人工智能学院",
#             'term': "term1",
#             'state': state
#         })

#         state = getstate(year, i, "term2")
#         files.append({
#             'year': year,
#             'grade': str(i),
#             'college': "大数据与人工智能学院",
#             'term': "term2",
#             'state': state
#         })
#     return jsonify(files)
term_names={
    'term1':'第一学期',
    'term2':'第二学期'
}
@api_blue.route('/data/delete', methods=['POST'])
@login_required
def delete_file():
    if request.method == 'POST':
        # aa=requests.get('http://127.0.0.1:5000/delete?filename=aa.xls')
        uploadfile , datafile=  getuploadpath( request.json)
        year = request.json['year']
        grade = request.json['grade']
        term = request.json['term']

        #学院
        college=request.json['college']

        if term in term_names.keys():
            term = term_names[term]
        # timestamp = request.args.get('timestamp')
        # logger.debug('delete file : %s, timestamp is %s' % (filename, timestamp))
        try:
            fullfile = os.path.join(UPLOAD_PATH,uploadfile)
            if os.path.exists(fullfile):
                os.remove(fullfile)
            fullfile = os.path.join(UPDATA_PATH,datafile)
            if os.path.exists(fullfile):
                os.remove(fullfile)
            print("delete from bigdata where college='{college}' year='{year}' and grade='{grade}' and semester='{term}'".format(year=year,term=term,grade=grade,college=college))
            result=Bigtable.query.filter(Bigtable.year==year).delete()
            db.session.commit()
            return api_result(0,msg="删除数据成功，删除条数:"+str(result))
            # database
        except Exception as e:

            return api_result(-1,msg="删除数据失败:"+str(e))

    else:
        return api_result(-1,msg="method not allow")

