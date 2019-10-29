# feedback_course<img src="https://github.com/shawnco411/Data_Structure/blob/master/shawnco4111.png" width="6%" align="right">
面向课程的个性化学生反馈系统

## 项目简介

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/home.PNG" title="主页">

* 本项目是为了提升教育机构对学生的管理水平与效率、为了充分反馈学生需求并制定个性化教育方针而建立的面向课程的个性化学生反馈系统。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/course.png" title="课程详情">

* 用户可以在本系统注册、登录、登出、编辑个人信息、下载作业、发起讨论、删除讨论、回复消息、删除回复、下载资源等。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/homework.png" title="作业列表">

* 学生用户还可以提交作业、选课、退课等；教师用户还可以创建课程、选择助教、编辑课程信息、布置作业、删除课程、删除作业、作业评分、赋予助教权限、取消助教权限、移除助教等；助教用户还可以作业批改、编辑课程信息、上传课程资源、布置作业等。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/discuss.gif" title="讨论区">

## 主页交互

* 老师用户登陆后会在首页看到自己创建的所有课程，能够**进入课程讨论区**，**查看课程详情**，还可以执行“**添加课程**”操作。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/teacher.gif">

* 学生用户登陆后会在首页看到教务系统中的所有课程，能够执行“**选课**”操作和“**查看课程详情**”操作，选课后还可以**进入相应课程的讨论区**。

<img src="https://github.com/shawnco411/feedback_course/blob/master/doc/student.gif">

* 学生助教和专职助教的交互与学生类似，区别在于专职助教只能看到自己担任助教的课程且不能选课，学生助教可以看到所有课程但是不能选自己担任助教的课。

## 运行方法
* 第一步：在项目的文件夹下面（含有manage.py）,打开命令行输入：`python manage.py migrate`

* 第二步：命令行输入输入`python manage.py createsuperuser` 后控制台会输出地址，用浏览器访问此地址并成功打开网页后请在地址栏加上后缀/login以转到登录页面，首次使用需点击导航栏上的“注册”字样进行注册。

具体可参看：[Django项目运行方法](https://blog.csdn.net/dg_summer/article/details/77046294 "Django项目运行方法")

## 文档说明
* `/doc`目录下有[设计报告](https://github.com/shawnco411/feedback_course/blob/master/doc/%E8%AE%BE%E8%AE%A1%E6%8A%A5%E5%91%8A.pdf "设计报告")、[用户使用说明书](https://github.com/shawnco411/feedback_course/blob/master/doc/%E7%94%A8%E6%88%B7%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E4%B9%A6.pdf "用户使用说明书")、[需求规格书](https://github.com/shawnco411/feedback_course/blob/master/doc/%E9%9C%80%E6%B1%82%E8%A7%84%E6%A0%BC%E4%B9%A60.3.1.pdf "需求规格书")以及[阶段成果展示PPT](https://github.com/shawnco411/feedback_course/blob/master/doc/%E8%BD%AF%E5%B7%A5%E5%B1%95%E7%A4%BA_%E5%BF%BD%E9%AA%81.pptx "阶段成果展示PPT")，方便开发者和使用者查阅（若无法在线预览请下载查看）。

## 运行环境
* Django           2.7.1
* Python            3.7.2
* PyMySQL        0.9.3
* mysql              8.0.15

## 注意事项
* When using in unix, use the code :Feedback/setting.py,line90-93
* Change the code:Feedback/setting.py,line86 to your own password
* If your debug info points to ’widget_tweaks’,use
`pip install django-widget-tweaks`
* Before you push something, use `git pull` first
* If you have any other attentions, please add here
* 发送邮件目前默认发件人是1262539334@qq.com，如需修改在settings.py末尾设置，需要获取邮箱的授权密码；注册用户的邮箱必须是真实邮箱，否则会报错。
*  If your debug info points to ’apscheduler’,use
`pip install django-apscheduler`

## AI环境要求
### use `pip install`  to install them
* pandas
* tensorflow
* keras
* jieba
* gensim
* sklearn

## 开源协议 

[GNU General Public License v3.0](LICENSE)

