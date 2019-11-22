import os
import re

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import xlrd

# connent=create_engine('mysql+pymysql://root:root@localhost:3306/reads_table?charset=utf8')
'''
测试智能读取数据,不管里面有多少个sheet
'''

need_columns = [
    ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处提供）', '综合素质测评分（P2)', '排名','班级'],
    ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处提供）', '综合成绩', '排名', '班级'],
    ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处导出）', '综合素质测评分', '排名', '班级'],
]
need_word={
            '学号':'style_id',
            '姓名':'stu_name',
            '思想政治':'political_edu',
            '身心健康':'physical_heal',
            '创新创业':'innovation_entrep',
            '技术技能':'technical_skills',
            '志愿服务':'volunte',
            '人文艺术':'human_art',
            '综合素质理论':'zh_theory',
            '总分':'score',
            'GPA(教务处提供）':'GPA',
            '综合成绩':'zh_score',
            '班级':'class',
            '年级':'year',
            '学期':'semester',
}

key=list(need_word.keys())

CURRENT = os.path.dirname(os.path.dirname(__file__))
UPLOAD_PATH = CURRENT + '/uploads/static/'
UPDATA_PATH = CURRENT + '/uploads/updata'


filess = ['2018-2019学年度第二学期学生综合素质测评分（2017级）.xls', '2018-2019学年度第一学期学生综合素质测评分（2017级）.xls',
         '2018-2019学年度第二学期学生综合素质测评分（2018级）.xls', '2018-2019学年度第一学期学生综合素质测评分（2018级）.xls']

# 循环数据文件
filename='2018-2019学年度第二学期学生综合素质测评分（2018级）.xls'
files=UPLOAD_PATH+filename

save_csv=UPDATA_PATH+filename.split('.')[0]+'.csv'

excel = pd.ExcelFile(files)
big_data_name = excel.sheet_names  # 拿到所有的sheetname

for needs in need_columns:  # 循环所有可能出现的表头
    #增加多两列数据
    for i in big_data_name:  # 循环所有的sheetname
        data = pd.read_excel(files, sheet_name=i, header=2)
        headers = data.columns.values.tolist()  # 将表头转换成列表的形式
        if headers == needs:  # 将可能出现的表头与excel里面的header对应
            # sheet_name = '大数据'  # 成功就将其表头转换成大数据
            data = data.drop(columns=['排名'])  # 删除排名
            #print(data.head(2))
            data['年级'] = re.findall('\w+级', filename)[0]  # 参数expand=True在一组返回值的情况下，返回数据框
            data['学期'] = re.findall('.*?(第.*?期).*?', filename)[0]
    #         #data.to_excel(file_path, header=2, index=False)
            head = data.columns.tolist()
            app = []
            for i in range(0, len(key)):
                if head[i] == key[i]:
                    pass
                else:
                    head[i] = key[i]

            for i in head:
                app.append(need_word[i])
            data.columns = app
            data.to_csv(save_csv, encoding='utf-8', index=False)
            print(data.head(2))
        
            
            
# excels=pd.read_excel(files,header=2)
# print(excels.shape)
# print(excels.columns)
