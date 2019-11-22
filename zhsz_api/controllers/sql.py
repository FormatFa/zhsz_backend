from flask import  jsonify,request
from . import  db
from . import api_blue
from  zhsz_api.models import db as db2

#班级图所需要的数据

@api_blue.route('/banji', methods=['POST'])
# @login_required
def banji():
    '''
    requests.post("http://127.0.0.1:5000/select/banji",
    json={"year":2018,"term":"term1","classid":"17大数据1","college":"大数据与人工智能学院"})
    '''
    if request.method == 'POST':
        formdata= request.json
        print(formdata)
        class_name = formdata['classid']
        semester=formdata['term']
        
        if formdata['term']=="term1":
            semester="第一学期"
        elif formdata['term']=="term2":
            semester="第二学期"

        year = formdata.get('year')
        college=formdata.get('college')
        print(college)
        filter_str=''
        if semester=='year':
            filter_str='and year="{}"'.format(year)
        else:
            filter_str='and semester="{}" and year="{}"'.format(semester,year)


        # if class_name=='17云计算1' :

        # 1--
        people = 'select count(distinct style_id) from zhsz where gk_class="{}" and college="{}";'.format(class_name,college)
        print(people)
        db.execute(people)
        students_num = db.fetchone()[0]
        classjbCard = {
            "classname": class_name,
            "students": students_num
        }

        # 2--
        # if semester=='第一学期':
        one_zh_score = 'select avg(zh_score) from zhsz where gk_class="{}" and semester="第一学期" and college="{}";'.format(class_name,college)
        db.execute(one_zh_score)
        term1_score = db.fetchone()[0]

        # one_zh_rank='select s.gk_class,s.semester,s.zh,(select count(distinct zh) from (select avg(zh_score) as zh from zhsz group by gk_class)as a where zh>=s.zh)as rank from (select semester,gk_class,avg(zh_score) as zh from zhsz group by gk_class,semester)as s where gk_class="{}" and semester="第一学期" order by s.zh desc;'.format(class_name)
        one_zh_rank = 'select s.year,s.semester,s.gk_class,s.zh,' \
                      'count(distinct a.zh) from (select year,semester,gk_class,avg(zh_score) as zh ' \
                      'from zhsz where year="{}" and semester="第一学期" group by gk_class,year )as s ' \
                      'join (select year,gk_class,avg(zh_score) as zh from zhsz where year="{}" and semester="第一学期" and college="{}" ' \
                      'group by gk_class,year) as a on s.zh <= a.zh where s.gk_class="{}" and s.year="{}" ' \
                      'group by s.gk_class,s.year  order by s.zh desc;'.format(year, year, college,class_name, year)

        db.execute(one_zh_rank)
        print(one_zh_rank)
        term1_paiming = db.fetchall()[0]

        # 第二学期
        two_zh_score = 'select avg(zh_score) from zhsz where gk_class="{}" and semester="第二学期";'.format(class_name)
        db.execute(two_zh_score)
        term2_score = db.fetchone()[0]

        two_zh_rank = 'select s.year,s.semester,s.gk_class,s.zh,' \
                      'count(distinct a.zh) from (select year,semester,gk_class,avg(zh_score) as zh ' \
                      'from zhsz where year="{}" and semester="第二学期" group by gk_class,year )as s ' \
                      'join (select year,gk_class,avg(zh_score) as zh from zhsz where year="{}" and semester="第二学期" and college="{}" ' \
                      'group by gk_class,year) as a on s.zh <= a.zh where s.gk_class="{}" and s.year="{}" ' \
                      'group by s.gk_class,s.year  order by s.zh desc;'.format(year, year,college, class_name, year)
        print(two_zh_rank)
        db.execute(two_zh_rank)
        term2_paiming="数据不存在"
        temp = db.fetchall()
        if len(temp)>0:
            term2_paiming = temp[0]

        classCard = {
            "term1_score": term1_score,  # 第一学期的综合素平均分
            "term2_score": term2_score,  # 第二学期的综合素平均分
            "term1_paiming": term1_paiming,  # 第一学期在全院的排名
            "term2_paiming": term2_paiming  # 第二学期在全院的排名
            # https://blog.csdn.net/shiwodecuo/article/details/54632839
            # https://blog.csdn.net/qq1032350287/article/details/86693068
        }


        # 3---
        # 整个年度，不管学期
        grade = "20" + class_name[:2]

        college_value = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from zhsz WHERE college="{}" and grade="{}" {};'.format(college,grade, filter_str)
        class_value = 'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from zhsz WHERE college="{}" and gk_class="{}" {};'.format(college,class_name, filter_str)

        print(college_value)
        db.execute(college_value)
        CollegeValue = db.fetchall()[0]

        db.execute(class_value)
        ClassValue = db.fetchall()[0]

        suchindexscores = [
                         {
                             'value':CollegeValue,'name':'学院指标平均分'
                         },
                         {
                             'value':ClassValue,'name':'班级指标平均分'
                         }]

        # 4---改成distinct
        student_name = ' select distinct stu_name from zhsz where college="{}" and gk_class="{}" and year="{}" ;'.format(college,class_name, year)
        stu_name_app = []
        db.execute(student_name)
        StudentName = db.fetchall()
        for stuName in StudentName:
            stu_name_app.append(stuName[0])
        students = {
            "student": stu_name_app
        }

        # 5---
        indexs = {'political_edu': '思想政治', 'physical_heal': "身心健康", 'innovation_entrep': '创新创业',
                  'technical_skills': '技术技能', 'volunte': '志愿服务', 'human_art': '人文艺术', 'zh_theory': '综合素质理论','zh_score':"总分Top5"}



        topstudent = {}
        for key, value in indexs.items():
            name_app = []
            score_app = []
            all_sql = 'select stu_name,{} from zhsz where college="{}" and gk_class="{}" {filter_str} order by {} desc limit 5;'.format(key, college,class_name, key,filter_str=filter_str)
            db.execute(all_sql)
            allName = db.fetchall()
            print('all',all_sql)

            for name, score in allName:
                name_app.append(name)
                score_app.append(score)

            topstudent[value] = {
                'names': name_app,
                'scores': score_app
            }

        # 6-
        total_sql = 'select count(stu_name),CASE ' \
                    'when score >= 0 and score <= 10 THEN "0-10" ' \
                    'when score > 10 and score <= 20 THEN "11-20" ' \
                    'when score > 20 and score <= 30 THEN "21-30" ' \
                    'when score > 30 and score <= 40 THEN "31-40" ' \
                    'when score > 40 and score <=50 THEN "41-50"  ' \
                    'when score>50 THEN "50以上"  end as "总分区间" from zhsz ' \
                    'where college="{}" and gk_class="{}" {filter_str} ' \
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
                    'when score>50 THEN "50以上"  end;'.format(college,class_name, filter_str=filter_str)

        db.execute(total_sql)
        TotalScores = db.fetchall()
        allscores = []
        total_app = []
        for people, total in TotalScores:
            total_score = {}
            total_score['value'] = people
            total_score['name'] = total
            allscores.append(total_score)
            total_app.append(total)

        totalscores = {
            "ranges": total_app,
            "allscores": allscores
        }

        return jsonify(
            {"classjbCard": classjbCard, "classCard": classCard, "suchindexscores": suchindexscores, "students": students,
             "topstudent": topstudent, "totalscores": totalscores})




@api_blue.route('/geren', methods=['POST'])
# @login_required
def geren():
    if request.method == 'POST':

        formdata = request.json
        
        year = formdata.get('year')
        stu_name = formdata.get('stu_id')
        class_name = formdata.get('classid')
        college=formdata.get('college')
        if formdata['term']=="term1":
            semester="第一学期"
        elif formdata['term']=="term2":
            semester="第二学期"

        if formdata['term']=='year':
        # 年度的什么都不过滤
            filter_sql = 'year="{}"'.format(year)
        else:
            # 学期的就过滤学期
            
            filter_sql = 'year="{}" and semester="{}"'.format(year,semester)
        
        # 特殊处理
       


        # 1--
        stu_score = 'select zh_score from zhsz where stu_name="{}" and semester="第一学期" and year="{}" and college="{}";'.format(
            stu_name, year,college)
        db.execute(stu_score)

        term1_avlscore = db.fetchall()[0][0]

        stu_yuan_rank = 'select (select count(distinct zh) from (select zh_score as zh from zhsz where semester="第一学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from zhsz where semester="第一学期" and year="{}" and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(year, year,college, stu_name)
        db.execute(stu_yuan_rank)
        print("stu_yuan_rank",stu_yuan_rank)
        term1_yranking = db.fetchone()[0]
        stu_class_rank = 'select (select count(distinct zh) from (select zh_score as zh from zhsz where gk_class="{}" and semester="第一学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from zhsz where gk_class="{}" and semester="第一学期" and year="{}" and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(class_name, year, class_name, year, college,stu_name)
        db.execute(stu_class_rank)
        term1_cranking = db.fetchone()[0]
        studentCard1 = {
            "term1_avlscore": term1_avlscore,  ##第一学期综合素质平均分
            "term1_yranking": term1_yranking,  ##第一学期综合素质在全院排名
            "term1_cranking": term1_cranking  ##第一学期综合素质在全班排名
        }

        # 1_1--
        stu_score_2 = 'select zh_score from zhsz where stu_name="{}" and semester="第二学期" and year="{}" and college="{}";'.format(
            stu_name, year,college)
        db.execute(stu_score_2)

        term2_avlscore = "无此学期数据"
        temp = db.fetchall()
        if len(temp)>0:
            term2_avlscore=temp[0][0]
        stu_yuan_rank_2 = 'select (select count(distinct zh) from (select zh_score as zh from zhsz where semester="第二学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from zhsz where semester="第二学期" and year="{}" and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            year, year, college,stu_name)

        db.execute(stu_yuan_rank_2)
        term2_yranking = "无此学期数据"
        temp = db.fetchone()
        if not temp ==None:
            term2_yranking=temp[0]
        
        stu_class_rank_2 = 'select (select count(distinct zh) from (select zh_score as zh from zhsz where gk_class="{}" and semester="第二学期" and year="{}") as a where zh>=s.zh) as "rank" from (select stu_name,zh_score as zh from zhsz where gk_class="{}" and semester="第二学期" and year="{}" and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(
            class_name, year, class_name, year, college,stu_name)
        db.execute(stu_class_rank_2)
        temp = db.fetchone()
        term2_cranking = "无此学期数据" if temp == None else temp[0] 
        studentCard2 = {
            "term2_avlscore": term2_avlscore,  ##第二学期综合素质平均分
            "term2_yranking": term2_yranking,  ##第二学期综合素质在全院排名
            "term2_cranking": term2_cranking  ##第二学期综合素质在全班排名
        }

        # 2--
        stu_zhibiao_score = db2.session.execute(
            'select political_edu,physical_heal,innovation_entrep,technical_skills,volunte,human_art,zh_theory from zhsz where stu_name="{}" and {filter_sql} and college="{}";'.format(
                stu_name ,college,filter_sql=filter_sql)).fetchone()
        print("学生指标sql:",'select political_edu,physical_heal,innovation_entrep,technical_skills,volunte,human_art,zh_theory from zhsz where stu_name="{}" and {filter_sql} and college="{}";'.format(
                stu_name, college,filter_sql=filter_sql))
        class_zhibiao_avg_score = db2.session.execute(
            'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from zhsz where gk_class="{}" and {filter_sql} and college="{}";'.format(
                class_name,college,filter_sql=filter_sql))
        yuan_zhibiao_avg_score = db2.session.execute(
            'select avg(political_edu),avg(physical_heal),avg(innovation_entrep),avg(technical_skills),avg(volunte),avg(human_art),avg(zh_theory) from zhsz where  college="{}" and {filter_sql};'.format(
                college,filter_sql=filter_sql))
        suchscores = []
        suchscores2 = []
        suchscores3 = []
        name1 = '学院指标平均分'
        name2 = '班级指标平均分'
        name3 = '学生指标分数'
        if stu_zhibiao_score is not  None:
            for i in stu_zhibiao_score:
                suchscores.append(i)
        for i_1 in class_zhibiao_avg_score:
            suchscores2.append(i_1)
        for i_2 in yuan_zhibiao_avg_score:
            suchscores3.append(i_2)

        suchindex = [{
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
      ##各指标雷达

        # 3--
        indexs = {'political_edu': '思想政治', 'physical_heal': "身心健康", 'innovation_entrep': '创新创业',
                  'technical_skills': '技术技能', 'volunte': '志愿服务', 'human_art': '人文艺术', 'zh_theory': '综合素质理论'}
        yuanData = []
        ClassData = []
        for key, value in indexs.items():
            score = db2.session.execute(
                'select {} from zhsz where stu_name="{}" and {filter_sql} and college="{}";'.format(key,
                                                                                                     stu_name,
                                                                                                     college ,filter_sql=filter_sql ) ).fetchone()
            rank = db2.session.execute(
                'select (select count(distinct zh) from (select {} as zh from zhsz where {filter_sql}) as a where zh>=s.zh) as "rank" from (select stu_name,{} as zh from zhsz where {filter_sql} and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(
                    key, key, college,stu_name,filter_sql=filter_sql )).fetchone()

            if score is not None:
                yuanData.append({
                'Collegindex': value,
                'Collegscores': score[0],
                'Collegranking': rank[0]
            })
        print("yuanData",yuanData)


        for key1, value1 in indexs.items():
            sql_score1='select {} from zhsz where stu_name="{}" and {filter_sql} and gk_class="{}" and college="{}";'.format(key1, stu_name,class_name,college,filter_sql=filter_sql)
            print("sql_score1",sql_score1)
            score1 = db2.session.execute(sql_score1).fetchone()
            print('score1',score1)
            rank1 = db2.session.execute(
                'select (select count(distinct zh) from (select {} as zh from zhsz where gk_class="{}" and {filter_sql}) as a where zh>=s.zh) as "rank" from (select stu_name,{} as zh from zhsz where gk_class="{}" and {filter_sql} and college="{}") as s where stu_name="{}" order by s.zh desc;'.format(
                    key1, class_name, key1, class_name,  college,stu_name,filter_sql=filter_sql)).fetchone()
            if score1 is not None:
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
            {"studentCard1": studentCard1, "studentCard2": studentCard2, "suchindexscores": suchindex, "data1": data1,
             "data2": data2})



