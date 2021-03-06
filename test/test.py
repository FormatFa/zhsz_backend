from flask import jsonify
from flask import Flask,request
from SQL_All import db
#
from  CreateUser.models import db as db2
app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root@127.0.0.1:3306/GK_ZH"
db2.init_app(app)
@app.route('/banji', methods=['GET'])
def banji():
    if request.method=='GET':
        class_name=request.args.get('class_name')
        semester=request.args.get('semester')
        year=request.args.get('year')
        "127.0.0.1:5000:/banji?class_name=17dashuju&semester=d&year="

        #if class_name=='17云计算1' :

        #1--
        people='select count(distinct style_id) from bigdata where gk_class="{}";'.format(class_name)
        db.execute(people)
        students_num=db.fetchone()[0]
        classjbCard={
            "classname": class_name,
            "students": students_num
        }

        #2--
        #if semester=='第一学期':
        one_zh_score='select avg(zh_score) from bigdata where gk_class="{}" and semester="第一学期";'.format(class_name)
        db.execute(one_zh_score)
        term1_score=db.fetchone()[0]


        #one_zh_rank='select s.gk_class,s.semester,s.zh,(select count(distinct zh) from (select avg(zh_score) as zh from bigdata group by gk_class)as a where zh>=s.zh)as rank from (select semester,gk_class,avg(zh_score) as zh from bigdata group by gk_class,semester)as s where gk_class="{}" and semester="第一学期" order by s.zh desc;'.format(class_name)
        one_zh_rank = 'select s.year,s.semester,s.gk_class,s.zh,' \
                      'count(distinct a.zh) from (select year,semester,gk_class,avg(zh_score) as zh ' \
                      'from bigdata where year="{}" and semester="第一学期" group by gk_class,year )as s ' \
                      'join (select year,gk_class,avg(zh_score) as zh from bigdata where year="{}" and semester="第一学期" ' \
                      'group by gk_class,year) as a on s.zh <= a.zh where s.gk_class="{}" and s.year="{}" ' \
                      'group by s.gk_class,s.year  order by s.zh desc;'.format(year,year,class_name,year)

        db.execute(one_zh_rank)
        term1_paiming=db.fetchall()[0]


        #第二学期
        two_zh_score = 'select avg(zh_score) from bigdata where gk_class="{}" and semester="第二学期";'.format(class_name)
        db.execute(two_zh_score)
        term2_score = db.fetchone()[0]


        two_zh_rank = 'select s.year,s.semester,s.gk_class,s.zh,' \
                      'count(distinct a.zh) from (select year,semester,gk_class,avg(zh_score) as zh ' \
                      'from bigdata where year="{}" and semester="第二学期" group by gk_class,year )as s ' \
                      'join (select year,gk_class,avg(zh_score) as zh from bigdata where year="{}" and semester="第二学期" ' \
                      'group by gk_class,year) as a on s.zh <= a.zh where s.gk_class="{}" and s.year="{}" ' \
                      'group by s.gk_class,s.year  order by s.zh desc;'.format(year, year, class_name, year)
        print(two_zh_rank)
        db.execute(two_zh_rank)
        term2_paiming = db.fetchall()[0]

        classCard = {
            "term1_score": term1_score,  # 第一学期的综合素平均分
            "term2_score":term2_score,  #第二学期的综合素平均分
            "term1_paiming": term1_paiming,  # 第一学期在全院的排名
            "term2_paiming":term2_paiming #第二学期在全院的排名
                                # https://blog.csdn.net/shiwodecuo/article/details/54632839
                                #https://blog.csdn.net/qq1032350287/article/details/86693068
        }


        '''
        你搞定
        
        '''
        #3---
        #整个年度，不管学期
        grade = "20" + class_name[:2]
        if semester == "year" :
            college_value='select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata WHERE year="{}" AND grade="{}";'.format(year,grade)
            class_value = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata WHERE gk_class="{}" AND year="{}";'.format(class_name,year)

        #传入学期
        else:
            college_value = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata WHERE grade="{}" AND semester="{}" AND year="{}";'.format(grade, semester,year)
            class_value = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata WHERE gk_class="{}" AND semester="{}" AND year="{}";'.format(class_name,semester,year)


        db.execute(college_value)
        CollegeValue=db.fetchall()[0]

        db.execute(class_value)
        ClassValue = db.fetchall()[0]


        suchindexscores= {
                    "CollegeValue": CollegeValue,
                    "ClassValue": ClassValue
                         },


        #4---
        student_name=' select stu_name from bigdata where gk_class="{}" and semester="第二学期" and year="{}";'.format(class_name,year)
        stu_name_app=[]
        db.execute(student_name)
        StudentName=db.fetchall()
        for stuName in StudentName:
            stu_name_app.append(stuName[0])
        students={
            "student":stu_name_app
        }


        #5---
        indexs = {'political_edu': '思想政治', 'physical_heal': "身心健康", 'innovation_entrep': '创新创业',
                  'technical_skills': '技术技能', 'volunte': '志愿服务', 'human_art': '人文艺术', 'zh_theory': '综合素质理论'}

        topstudent={}
        for key, value in indexs.items():
            name_app=[]
            score_app=[]
            all_sql='select stu_name,{} from bigdata where gk_class="{}" and semester="{}" and year="{}" order by {} desc limit 5;'.format(key,class_name,semester,year,key)
            db.execute(all_sql)
            allName=db.fetchall()

            for name,score in allName:
                name_app.append(name)
                score_app.append(score)

            topstudent[value] = {
                'names':name_app ,
                'scores': score_app
            }

        #6-
        total_sql='select count(stu_name),CASE ' \
              'when score >= 0 and score <= 10 THEN "0-10" ' \
              'when score > 10 and score <= 20 THEN "11-20" ' \
              'when score > 20 and score <= 30 THEN "21-30" ' \
              'when score > 30 and score <= 40 THEN "31-40" ' \
              'when score > 40 and score <=50 THEN "41-50"  ' \
              'when score>50 THEN "50以上"  end as "总分区间" from bigdata ' \
              'where gk_class="{}" and semester="{}" and year="{}" ' \
              'group by CASE when score >= 0 and score <= 10 THEN "0-10" ' \
              'when score > 10 and score <= 20 THEN "11-20" ' \
              'when score > 20 and score <= 30 THEN "21-30" ' \
              'when score > 30 and score <= 40 THEN "31-40" ' \
              'when score > 40 and score <=50 THEN "41-50"  ' \
              'when score>50 THEN "50以上" end ' \
              'order by CASE when score >= 0 and score <= 10 THEN "0-10" ' \
              'when score > 10 and score <= 20 THEN "11-20" ' \
              'when score > 20 and score <= 30 THEN "21-30" ' \
              'when score > 30 and score <= 40 THEN "31-40" ' \
              'when score > 40 and score <=50 THEN "41-50"  ' \
              'when score>50 THEN "50以上"  end;'.format(class_name,semester,year)

        db.execute(total_sql)
        TotalScores = db.fetchall()
        print(TotalScores)
        allscores=[]
        total_app=[]

        for people,total in TotalScores:
            total_score = {}
            total_score['value']=people
            total_score['name']=total
            allscores.append(total_score)

            total_app.append(total)
        print(allscores)

        totalscores={
            "ranges":total_app,
            "allscores":allscores
        }


        return jsonify({"ClassData": classjbCard, "classCard": classCard,"suchindexscores":suchindexscores,"student":students,"tostudent":topstudent,"totalscores":totalscores})

        # elif semester=='第二学期':
        #     one_zh_score = 'select avg(zh_score) from bigdata where gk_class="{}" and semester="{}";'.format(class_name, semester)
        #     db.execute(one_zh_score)
        #     term1_score = db.fetchone()[0]
        #     classCard={
        #     "term1_score": term1_score, #第一学期的综合素平均分
        #     "term2_score": 1, #第二学期的综合素平均分
        #     "term1_paiming": 9, #第一学期在全院的排名
        #     "term2_paiming": 6 #第二学期在全院的排名
        # }
        #
        #     print(classjbCard)
        #     return jsonify({"ClassData":classjbCard,"classCard":classCard})


@app.route('/geren', methods=['GET'])
def geren():
    if request.method=='GET':
        semester = request.args.get('semester')
        year = request.args.get('year')
        stu_name = request.args.get('stu_id')
        class_name = request.args.get('class_name')

        print(stu_name)
        # 1--
        stu_score = 'select zh_score from bigdata where stu_name="{}" and semester="第一学期" and year="{}";'.format(stu_name, year)
        print(stu_score)
        db.execute(stu_score)

        term1_avlscore = db.fetchall()[0]
        print(term1_avlscore)
        stu_yuan_rank = 'select (select count(distinct zh) from (select zh_score as zh from bigdata where semester="第一学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from bigdata where semester="第一学期" and year="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            year, year, stu_name)
        db.execute(stu_yuan_rank)
        term1_yranking = db.fetchone()[0]
        stu_class_rank = 'select (select count(distinct zh) from (select zh_score as zh from bigdata where gk_class="{}" and semester="第一学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from bigdata where gk_class="{}" and semester="第一学期" and year="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            class_name, year, class_name, year, stu_name)
        db.execute(stu_class_rank)
        term1_cranking = db.fetchone()[0]
        studentCard1 = {
            "term1_avlscore": term1_avlscore,  ##第一学期综合素质平均分
            "term1_yranking": term1_yranking,  ##第一学期综合素质在全院排名
            "term1_cranking": term1_cranking  ##第一学期综合素质在全班排名
        }

        # 1_1--
        stu_score_2 = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata where stu_name="{}" and semester="第二学期" and year="{}";'.format(
            stu_name, year)
        db.execute(stu_score_2)
        term2_avlscore = db.fetchall()[0]
        stu_yuan_rank_2 = 'select (select count(distinct zh) from (select zh_score as zh from bigdata where semester="第二学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from bigdata where semester="第二学期" and year="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            year, year, stu_name)
        db.execute(stu_yuan_rank_2)
        term2_yranking = db.fetchone()[0]
        stu_class_rank_2 = 'select (select count(distinct zh) from (select zh_score as zh from bigdata where gk_class="{}" and semester="第二学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from bigdata where gk_class="{}" and semester="第二学期" and year="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            class_name, year, class_name, year, stu_name)
        db.execute(stu_class_rank_2)
        term2_cranking = db.fetchone()[0]
        studentCard2 = {
            "term2_avlscore": term2_avlscore,  ##第二学期综合素质平均分
            "term2_yranking": term2_yranking,  ##第二学期综合素质在全院排名
            "term2_cranking": term2_cranking  ##第二学期综合素质在全班排名
        }

        # 2--
        stu_zhibiao_score = db2.session.execute(
            'select political_edu,physical_heal,innovation_entrep,technical_skills,volunte,human_art,zh_theory from bigdata where stu_name="{}" and year="{}" and semester="{}";'.format(
                stu_name, year, semester)).fetchone()
        class_zhibiao_avg_score = db2.session.execute(
            'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata where gk_class="{}" and year="{}" and semester="{}";'.format(
                class_name, year, semester))
        yuan_zhibiao_avg_score = db2.session.execute(
            'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from bigdata where year="{}" and semester="{}";'.format(
                year, semester))
        suchscores = []
        suchscores2 = []
        suchscores3 = []
        name1 = '学院指标平均分'
        name2 = '班级指标平均分'
        name3 = '学生指标分数'
        for i in stu_zhibiao_score:
            suchscores.append(i)
        for i_1 in class_zhibiao_avg_score:
            suchscores2.append(i_1)
        for i_2 in yuan_zhibiao_avg_score:
            suchscores3.append(i_2)

        suchindex = {
            'suchindexscores': [{
                'value': list(suchscores3[0].itervalues()),
                'name': name1
            }, {
                'value': list(suchscores2[0].itervalues()),
                'name': name2
            }, {
                'value': suchscores,
                'name': name3
            }
            ]
        }  ##各指标雷达

        # 3--
        indexs = {'political_edu': '思想政治', 'physical_heal': "身心健康", 'innovation_entrep': '创新创业',
                  'technical_skills': '技术技能', 'volunte': '志愿服务', 'human_art': '人文艺术', 'zh_theory': '综合素质理论'}
        yuanData = []
        ClassData = []
        for key, value in indexs.items():
            score = db2.session.execute(
                'select {} from bigdata where stu_name="{}" and year="{}" and semester="{}";'.format(key,
                                                                                                     stu_name,
                                                                                                     year,
                                                                                                     semester)).fetchone()
            rank = db2.session.execute(
                'select (select count(distinct zh) from (select {} as zh from bigdata where year="{}" and semester="{}") as a where zh>=s.zh) as "rank" from (select stu_name,{} as zh from bigdata where year="{}" and semester="{}") as s where stu_name="{}" order by s.zh desc;'.format(
                    key, year, semester, key, year, semester, stu_name)).fetchone()
            yuanData.append({
                'Collegindex': value,
                'Collegscores': score[0],
                'Collegranking': rank[0]
            })
        for key1, value1 in indexs.items():
            score1 = db2.session.execute(
                'select {} from bigdata where stu_name="{}" and year="{}" and semester="{}";'.format(key1, stu_name,
                                                                                                     year,
                                                                                                     semester)).fetchone()
            rank1 = db2.session.execute(
                'select (select count(distinct zh) from (select {} as zh from bigdata where gk_class="{}" and year="{}" and semester="{}") as a where zh>=s.zh) as "rank" from (select stu_name,{} as zh from bigdata where gk_class="{}" and year="{}" and semester="{}") as s where stu_name="{}" order by s.zh desc;'.format(
                    key1, class_name, year, semester, key1, class_name, year, semester, stu_name)).fetchone()
            ClassData.append({
                'Classindex': value1,
                'Classscores': score1[0],
                'Classranking': rank1[0]
            })
        data1 = {
            'CollegeData': yuanData  # 各指标在全院排名和各指标分数
        }
        data2 = {
            'ClassData': ClassData  # 各指标在全班排名和各指标分数
        }

        return jsonify(
            {"studentCard1": studentCard1, "studentCard2": studentCard2, "suchindex": suchindex, "data1": data1,
             "data2": data2})

if __name__ == '__main__':
    app.run(debug=True)


















