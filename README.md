### Flask 后台




## 配置安装

### 前提:
- 安装Python3
- 安装pip
- 设置pip源为阿里云的源(推荐)


下面命令在工程根目录执行

### 1. 创建虚拟环境
```
C:\Users\bigdata\Documents\zhsz\zhsz_flask>python -m venv venv

Linux:
[root@zhsz zhsz_flask]# python3 -m venv venv
```
使用PyCharm 或者 VSCode 等IDE ，就将工程的虚拟环境切换为刚才创建的虚拟环境(在工程根目录下)

### 2. pip安装依赖所需依赖

- 在终端里进入虚拟环境

```
windows 环境
(venv) C:\Users\bigdata\Documents\zhsz\zhsz_flask>venv\Scripts\activate
Linux 环境

[root@zhsz zhsz_flask]# source venv/bin/activate
(venv) [root@zhsz zhsz_flask]#
```
- 安装依赖
```
(venv) C:\Users\bigdata\Documents\zhsz\zhsz_flask>pip install -r requirements.txt
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting alembic==1.3.1 (from -r requirements.txt (line 1))
  Using cached https://mirrors.aliyun.com/pypi/packages/84/64/493c45119dce700a4b9eeecc436ef9e8835ab67bae6414f040cdc7b58f4b/alembic-1.3.1.tar.gz
Collecting astroid==2.3.3 (from -r requirements.txt (line 2))

```
 阿里云源 安装 flask_bcrypt 可能会失败, 尝试临时切换成原来的



## 初始化

### 配置数据库
修改settings.py文件 设置 ，设置 mysql的地址 和 用户名密码

### 初始化数据库

第一次运行执行下面命令
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

### 启动


python3  manage.py server



### 修改维护
生成requirements.txt
pip freeze > requirements.txt
