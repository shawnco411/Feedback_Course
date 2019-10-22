# feedback_course
面向课程的个性化学生反馈系统

# 项目简介

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/home.PNG">

本项目是为了提升教育机构对学生的管理水平与效率、为了充分反馈学生需求并制定个性化教育方针而建立的面向课程的个性化学生反馈系统。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/course.png">

用户可以在本系统注册、登录、登出、编辑个人信息、下载作业、发起讨论、删除讨论、回复消息、删除回复、下载资源等。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/homework.png">

学生用户还可以提交作业、选课、退课等；教师用户还可以创建课程、选择助教、编辑课程信息、布置作业、删除课程、删除作业、作业评分、赋予助教权限、取消助教权限、移除助教等；助教用户还可以作业批改、编辑课程信息、上传课程资源、布置作业等。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/feed.png">

# 运行方法
* 第一步：在项目的文件夹下面（含有manage.py）,打开命令行输入：`python manage.py migrate`
* 第二步：命令行输入输入`python manage.py createsuperuser` 之后控制台会输出地址，点击地址即可运行，注意进入网址后加后缀/login方可登陆，首次使用请点击导航栏上的“注册”字样进行注册。

具体可参看：[Django项目运行方法](https://blog.csdn.net/dg_summer/article/details/77046294 "Django项目运行方法")

# 运行环境
* Django           2.7.1
* Python            3.7.2
* PyMySQL        0.9.3
* mysql              8.0.15

# 注意事项
* When using in unix, use the code :Feedback/setting.py,line90-93
* Change the code:Feedback/setting.py,line86 to your own password
* If your debug info points to ’widget_tweaks’,use
`pip install django-widget-tweaks`
* Before you push something, use `git pull` first
* If you have any other attentions, please add here
* 发送邮件目前默认发件人是1262539334@qq.com，如需修改在settings.py末尾设置，需要获取邮箱的授权密码；注册用户的邮箱必须是真实邮箱，否则会报错。
*  If your debug info points to ’apscheduler’,use
`pip install django-apscheduler`

# AI环境要求
## use `pip install`  to install them
* pandas
* tensorflow
* keras
* jieba
* gensim
* sklearn
