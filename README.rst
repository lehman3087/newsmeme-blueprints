
newsmeme
========


项目说明
----------

该项目原来位于 https://bitbucket.org/danjac/newsmeme，属于 Flask 中 Powered By Flask （http://flask.pocoo.org/community/poweredby/）列表项目之一。

但是由于原作者已经不再更新代码了，随着 Flask 以及一些插件的升级，有些代码不能在新版本运行，因此需要对代码进行一些修改并且修复一些问题。

本项目为 Flask 开发 web 的经典项目，涉及到很多领域：
	
	* 用户管理(注册、登录、密码管理等等)
	* OpenID 登录
	* 社交系统(关注、取消关注、投票、评论、个人页等等)
	* 权限系统(用户、文章、评论以及投票各种权限设置等等)
	* 邮件系统
	* 数据库管理
	* and so on

安装&运行
-----------

1. 安装所需要的插件: 

	pip install -r requirements.txt

2. 安装 flask-themes:

    git https://github.com/maxcountryman/flask-themes.git 

    cd flask-themes or cd flask-themes-master

    python setup.py install


**这里需要特别提醒请勿用 pip install flask-themes 或者 easy_install flask-themes 来安装，因为版本有问题，可能会导致“提示无法找到模板文件”。**

3. 手动创建数据库，名称为 newsmeme.

4. 自动创建表:
	
	python manage.py createall

5. 运行 newsmeme:
	
	python manage.py runserver

6. 访问 http://127.0.0.1:5000/ 开始享受 newsmeme！


bug
-------

由于时间仓促，可能还存在未完全修复的地方，请直接发送邮件 sixu05202004@gmail.com 或者 Pull Requests，希望大家一起来努力维护该项目。
