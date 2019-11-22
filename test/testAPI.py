
import requests

# aa=requests.post("http://127.0.0.1:5000/auth/register",json={
#     'username':'linqiong',
#     'password':'12345678'
# })
# print(aa.text)
# bb=requests.post("http://127.0.0.1:5000/auth/login/alterPassword",json={
#     'username': 'big3',
#     'old_password':'12345678',
#     'password':'12345678a',
#     'password2':'12345678a'
# })
# print(bb.text)

# aa=requests.post("http://127.0.0.1:5000/auth/login",json={
#     'username':'big3',
#     'password':'12345678a'
# })
# print(aa.text)
# bb=requests.post("http://127.0.0.1:5000/auth/login/alterPassword",json={
#     'username': 'big2',
#     'old_password':'12345678',
#     'password':'zxcvbnmasd',
#     'password2':'zxcvbnmasd'
# })
# print(bb.text)

# abc=requests.post("http://127.0.0.1:5000/auth/login",json={
#     'username':'abcdfd',
#     'password':'abc111111d'
# })
# print(abc.text)
# aa=requests.post("http://127.0.0.1:5000/openid/test")
# print(aa)
# print(aa.text)
# print(os.path.dirname(os.path.dirname(__file__)))
# dangqian=os.path.dirname(os.path.dirname(__file__))
# UPLOAD_FOLDER = dangqian+'/uploads/static/'
# print(UPLOAD_FOLDER)
#
# files = {'file': open("2018-2019学年度第二学期学生综合素质测评分（2017级）.xls", 'rb')}
# print(files)
# res = requests.post('http://127.0.0.1:5000/folder/upload',data={"year":2018,"grade":2017,"term":"term2","college":"大数据与人工智能学院"}, files=files)

# print(res.text)
# print(res.text)
#
# aa=requests.post('http://127.0.0.1:5000/folder/handle',json={"year":2018,"grade":2017,"term":"term2","college":"大数据与人工智能学院"})
# print(aa.text)

#
# aa=requests.get('http://127.0.0.1:5000/folder/delete?filename=2018-2019学年度第二学期学生综合素质测评分（2018级）.xls')
# print(aa.text)
#
# sql=requests.get('http://127.0.0.1:5000/select/xueyuan')
# print(sql.text)


banji_sql=requests.post("http://127.0.0.1:5000/select/geren",json={"year":2018,"stu_id":"唐小煌","term":"term1","classid":"18大数据2","college":"大数据与人工智能学院"})
print(banji_sql.text)