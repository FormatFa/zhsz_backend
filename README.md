### 学生综合素质可视化分析 后端代码


前端项目地址:
https://gitee.com/old_tree/zhszweb

## 项目配置安装

### 前提:
- 安装Python3
- 安装pip
- 设置pip源为阿里云的源(推荐)
修改 ~/.pip/pip.conf（windows下为C:\Users\用户名\pip\pip.ini）文件(没有则新建)
文件里输入下面的配置
```
[global]

timeout = 6000

index-url = https://pypi.tuna.tsinghua.edu.cn/simple

trusted-host = pypi.tuna.tsinghua.edu.cn
```



下面命令在工程根目录执行

### 1. 创建虚拟环境
```
python3 -m venv venv
```
使用PyCharm 或者 VSCode 等IDE ，就将工程的虚拟环境切换为刚才创建的虚拟环境(在工程根目录下)

### 2. pip安装依赖所需依赖

- 在终端里进入虚拟环境

```
windows 环境
venv\Scripts\activate
Linux 环境
[root@zhsz zhsz_flask]# source venv/bin/activate
```

- 使用pip安装依赖库
```
pip install -r requirements.txt

```

## 初始化

### 1.配置数据库
修改`settings.py`文件  
设置 MySQL 的 地址 和 用户名密码

### 初始化数据库

第一次运行执行下面命令创建对应的表

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```



## 启动项目

使用命令
`python3  manage.py server`


### 修改维护

- 生成requirements.txt

`pip freeze > requirements.txt`


