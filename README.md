# feedback_course
A course-feedback system for soft engineering courses.

# Environment
* Django           2.7.1
* Python            3.7.2
* PyMySQL        0.9.3
* mysql              8.0.15

# Attention
* When using in unix, use the code :Feedback/setting.py,line90-93
* Change the code:Feedback/setting.py,line86 to your own password
* If your debug info points to ’widget_tweaks’,use
`pip install django-widget-tweaks`
* Before you push something, use `git pull` first
* If you have any other attentions, please add here
* 发送邮件目前默认发件人是1262539334@qq.com，如需修改在settings.py末尾设置，需要获取邮箱的授权密码；注册用户的邮箱必须是真实邮箱，否则会报错。
*  If your debug info points to ’apscheduler’,use
`pip install django-apscheduler`

# AI Environment Requirements
## use `pip install`  to install them
* pandas
* tensorflow
* keras
* jieba
* gensim
* sklearn