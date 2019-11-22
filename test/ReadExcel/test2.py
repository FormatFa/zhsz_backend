import os

import pandas as pd
import re
import xlwt
import xlrd
import pymysql
from sqlalchemy import create_engine
#智能导入系统

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
            '班级':'gk_class',
            '年级':'year',
            '学期':'semester',
}
key=list(need_word.keys())

DB_CONNECT_STRING = 'mysql+pymysql://root:root@localhost:3306/gk_zh?charset=utf8'
engine = create_engine(DB_CONNECT_STRING,echo=True)


files = '2018-2019学年度第二学期学生综合素质测评分（2017级）.xls'
CURRENT = os.path.dirname(os.path.dirname(__file__))

UPDATA_PATH = CURRENT + '/uploads/updata/'
file_path=UPDATA_PATH+files


save_csv=UPDATA_PATH+files.split('.')[0]+'.csv'
data=pd.read_excel(files,header=2,sheet_name='Sheet2',converters={u'学号':str})

print(data['学号'])

data=data.drop(columns=['排名'])
data['年级'] = re.findall('\w+级',files)[0] # 参数expand=True在一组返回值的情况下，返回数据框
data['学期'] = re.findall('.*?(第.*?期).*?', files)[0]

# data.to_excel(file_path,sheet_name="大数据",encoding='utf-8',header=2)
# print(data.head(2))
head=data.columns.tolist()
app=[]
for i in range(0, len(key)):
    if head[i] == key[i]:
        pass
    else:
        head[i] = key[i]

for i in head:
    app.append(need_word[i])
data.columns=app
#data.to_csv(save_csv,encoding='utf-8',index=False)
print(data.head(2))
#data.to_sql('bigdata', con=engine,if_exists='append',index=False)



# CURRENT=os.path.dirname(os.path.dirname(__file__))
# UPLOAD_PATH=CURRENT+'/uploads/static'
# files=os.path.join(UPLOAD_PATH, 'aa.xls')
# excel = pd.read_excel(files, header=2)
#
# print(excel.head(3))







#智能建议系统
