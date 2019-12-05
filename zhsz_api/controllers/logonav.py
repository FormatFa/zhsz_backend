# logo 导航 和学院界面的数据请求

from flask import Blueprint
# 
from zhsz_api.models import Bigtable
from  sqlalchemy import  *
from flask import request
from . import api_blue
# api_blue = Blueprint('nav',__name__,url_prefix='/nav')
import re
from flask_login import login_required
# query all class

def getListDict(list_dio,key,value):
    for item in list_dio:
        if item[key]==value:
            return item
    return None

# 查询数据库里所有的班级
@api_blue.route("/nav/classes",methods=['POST'])
@login_required
def get_classes():
    formdata = request.json
    print("请求班级数据:",formdata)
    # 指定学院的
    college = formdata['college']

    # print(help(distinct))
    result = Bigtable.query.with_entities( distinct( Bigtable.year)).all()
    years = [ i[0] for i in result]
    print("years:...",years)
    if len(years)==0:
        return {
            'code':-1,
            'msg':"year data zero!!"
        }
    if 'year' not in request.form:
        year=years[-1]
    else:
        year = request.js
    
    result = Bigtable.query.with_entities( distinct( Bigtable.year)).all()
    years = [ i[0] for i in result]
    print("years:...",years)


    result=Bigtable.query.with_entities( distinct( Bigtable.gk_class).label("class")).filter(Bigtable.college==college).all()
    
    classes = [ i[0] for i in result]
    # process to ..

    '''
     classes:[{
          label:"17", value:"17", children:[
            {label:"大数据",value:"bigdata"},
            {label:"云计算",value:"clound"}
          ]
      },
      {
         label:"18",value:"18",children:[{label:"大数据",value:"bigdata"},
            {label:"云计算",value:"clound"}]
      }
      ],
    '''
    results=[]
    for clazz in classes:
        print(clazz)
        items =[ i for i in  re.split("(\d+)",clazz) if i!=""]
        print(items)
        if len(items)!=3:
            print("error class name:",clazz)
        grade=items[0]
        classname = items[1]
        if len(items)>2:
            classnum = items[2]
        else:
            classnum='0'

        grade_dict = getListDict(results,'value',grade)
        if grade_dict is None:
            grade_dict={
                "value":grade,
                "label":grade,
                "children":[]

            }
            print(grade_dict)
            results.append(grade_dict)
        
        class_dict = getListDict(grade_dict['children'],'value',classname)
        if class_dict is None:
            class_dict={
                'value':classname,
                'label':classname,
                'children':[]
            }
            
            grade_dict['children'].append(class_dict)


        num_dict = getListDict(class_dict['children'],'value',classnum)
        if num_dict is None:

            num_dict={
                'value':classnum,
                'label':classnum,
                
            }
            class_dict['children'].append(num_dict)
    # query all year

  

    return {
        "data":{
            # 
            'classes':results,
            'years':years
        }
    }

term_names={
    'term1':'第一学期',
    'term2':'第二学期',
    # 'year':'年度'
}
@api_blue.route("/collage",methods=['POST'])
def collage():
    params = request.json
    year=params['year']
    term=params['term']
    college = params['college']
    if term in term_names.keys():
        term = term_names[term]
    print("request,arg",params)

    # filter term,year , college
    # (Bigtable.semester==params['term']
    if term=="year":
        filter_query = Bigtable.query.filter(Bigtable.year==year ,Bigtable.college==college)
    else:
        filter_query = Bigtable.query.filter( and_( Bigtable.year==year,Bigtable.semester==term   ),Bigtable.college==college)
    
    # Bigtable.query.

    # gpa_score
    result = {}
    temp = Bigtable.query.filter(Bigtable.college==college).with_entities(Bigtable.GPA,Bigtable.political_edu+Bigtable.physical_heal+Bigtable.innovation_entrep+Bigtable.technical_skills+Bigtable.volunte+Bigtable.human_art+Bigtable.zh_theory).all()
    print("len:",len(temp))
    gpas = []
    scores = []

    for i in temp:
        gpas.append(i[0])
        scores.append(i[1])
    gpa_score = {
        'gpas':gpas,
        'scores':scores
    }

    # ------------------------------range ---------------------
    myrange  = [10,20,30,40,50,60,70,80]

    range_text = [ "[{},{})".format(myrange[i],myrange[i+1]) for i in range(0,len(myrange)-1)]
    # less than 0
    range_text.insert(0,"[0,10)]")
    range_text.append("80+")
    print(range_text)
    ranges=[]
    print(func)
    term1_data  = Bigtable.query.filter(Bigtable.college==college, Bigtable.semester=="第一学期").with_entities(  func.interval( Bigtable.zh_score, *myrange).label("range"),func.count(1)).group_by('range').all()
    term1 = [0]*len(range_text)
    for item in term1_data:
        term1[item[0]] = item[1]

# range
    term2_data  = Bigtable.query.filter(Bigtable.college==college,Bigtable.semester=="第二学期").with_entities(  func.interval( Bigtable.zh_score, *myrange).label("range"),func.count(1)).group_by('range').all()
    term2 = [0]*len(range_text)
    for item in term2_data:
        term2[item[0]] = item[1]


    # print(term1)
    
    # print(term1_data)
# indexes
# all zhibiao
    indexnames= {
        'political_edu':"思想政治",
        'physical_heal':"身心健康",
		'innovation_entrep':"创新创业",
		'technical_skills':'技术技能',
		'volunte':'志愿服务',
		'human_art':'人文艺术',
		'zh_theory':'综合素质理论',
        'zh_score':"平均分"
		
    }
    
    # print([i for i in dir(Bigtable) if not i.startswith("_")])
    # get functio nhelp

   
    querycols = []
    for key,name in indexnames.items():
        querycols.append(  func.round(func.avg( getattr( Bigtable, key) ),2))
    scores = filter_query.with_entities(*querycols).first()
    indexes = {
        'indexes':list(indexnames.values()),
        'scores':list(scores)

    }
#---------------------------tops---------------------

    top={}
    # top 5 class
    temp = Bigtable.query.with_entities(Bigtable.gk_class,func.avg(Bigtable.human_art).label("score")).group_by(Bigtable.gk_class).order_by(desc(column("score"))).limit(5).all()
    # [('18云计算1', 5.73404255319149), ('18oracle', 5.531914893617022), ('17移动互联1', 5.027777777777778), ('18大数据2', 4.758196721311475), ('18云计算2', 4.458333333333333)]
    #top 50 student
    #zhijie na
    temp = Bigtable.query.with_entities(Bigtable.style_id,Bigtable.stu_name, func.round(func.avg(Bigtable.human_art),2).label("score")).group_by(Bigtable.style_id,Bigtable.stu_name).order_by(desc(column("score"))).limit(50).all()
    # print(temp)


    for key , name in indexnames.items():
        # column 
        col = getattr(Bigtable,key)
        temp = filter_query.with_entities(Bigtable.gk_class,func.round(func.avg(col),1).label("score")).group_by(Bigtable.gk_class).order_by(desc(column("score"))).limit(5).all()    
        classes = []
        students = []
        for i in temp:
            classes.append({
                'name':i[0],
                'score':i[1]
            })
        temp = filter_query.with_entities(Bigtable.style_id,Bigtable.stu_name,func.round(func.avg(col),1).label("score")).group_by(Bigtable.style_id,Bigtable.stu_name).order_by(desc(column("score"))).limit(50).all()
        for i in temp:
            students.append({
                'name':i[1],
                'id':i[0],
                'score':i[2]

            })
        top[name]={
            'classes':classes,
            'students':students
        }

    #---------------------card data-------------
    year_score=Bigtable.query.filter(Bigtable.year==year,Bigtable.college==college).with_entities(func.round(func.avg(Bigtable.zh_score),2)).scalar()
    term1_score = Bigtable.query.filter(Bigtable.college==college, and_( Bigtable.year==year,Bigtable.semester==term_names['term1'])).with_entities(func.round(func.avg(Bigtable.zh_score),2)).scalar()
    term2_score = Bigtable.query.filter(Bigtable.college==college, and_( Bigtable.year==year,Bigtable.semester==term_names['term2'])).with_entities(func.round(func.avg(Bigtable.zh_score),2)).scalar()

    # select year,semester,avg(zh_score ) from bigdata group by year,semester;
    #-------------------------trend-------------------

    result = Bigtable.query.with_entities(Bigtable.year,Bigtable.semester,func.avg(Bigtable.zh_score)).group_by(Bigtable.year,Bigtable.semester).all()
    print(result)

    years=[]
    term1_trend=[]
    term2_trend=[]
    # [('2018', '第一学期', 41.39818472268591), ('2018', '第二学期', 44.13349394817429)]
    # m
    for i in range(0,len(result),2):
        years.append(result[i][0])
        term1_trend.append(result[i][2])
        if i+1<len(result):
            term2_trend.append(result[i+1][2])



    return {
        'basicCard':{
            'year_score':year_score,
            'term1_score':term1_score,
            'term2_score':term2_score
        },
        'indexes':indexes,
        'gpa_score':gpa_score,
        'range':{
            'ranges':range_text,
            'term1_scores':term1,
            'term2_scores':term2
        },
        'top':top,
        'trend':{
            'years':years,
            'term1':term1_trend,
            'term2':term2_trend
        }

    }



