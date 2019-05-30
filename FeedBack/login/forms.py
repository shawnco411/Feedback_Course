from django import forms
from login.models import Homework,SubmitWork,Resource

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'userID'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'password'}))

class RegisterForm(forms.Form):
    idens = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('assistant', '助教'),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '例如: user123'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '建议6-16位包含字母数字'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '请和上一次输入相同'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': '例如: 123@qq.com'}))
    identity = forms.ChoiceField(label='身份', choices=idens)

    #captcha = CaptchaField(label='验证码')

class CreateCourseForm(forms.Form):
    locus = (
        ('(一)101', '(一）101'),
        ('(一)102', '(一）102'),
        ('(一)103', '(一）103'),
        ('(一)104', '(一）104'),
        ('(一)201', '(一）201'),
        ('(一)202', '(一）202'),
        ('(一)203', '(一）203'),
        ('(一)204', '(一）204'),
        ('(一)301', '(一）301'),
        ('(一)302', '(一）302'),
        ('(一)303', '(一）303'),
        ('(一)304', '(一）304'),
        ('(二)101', '(二）101'),
        ('(二)102', '(二）102'),
        ('(二)103', '(二）103'),
        ('(二)104', '(二）104'),
        ('(二)201', '(二）201'),
        ('(二)202', '(二）202'),
        ('(二)203', '(二）203'),
        ('(二)204', '(二）204'),
        ('(二)301', '(二）301'),
        ('(二)302', '(二）302'),
        ('(二)303', '(二）303'),
        ('(二)304', '(二）304'),
        ('(三)101', '(三）101'),
        ('(三)102', '(三）102'),
        ('(三)103', '(三）103'),
        ('(三)104', '(三）104'),
        ('(三)201', '(三）201'),
        ('(三)202', '(三）202'),
        ('(三)203', '(三）203'),
        ('(三)204', '(三）204'),
        ('(三)301', '(三）301'),
        ('(三)302', '(三）302'),
        ('(三)303', '(三）303'),
        ('(三)304', '(三）304'),
    )
    time = (
        ('周一1,2节', '周一1,2节'),
        ('周一3,4节', '周一3,4节'),
        ('周一5,6节', '周一5,6节'),
        ('周一7,8节', '周一7,8节'),
        ('周一9,10节', '周一9,10节'),
        ('周一11,12节', '周一11,12节'),
        ('周二1,2节', '周二1,2节'),
        ('周二3,4节', '周二3,4节'),
        ('周二5,6节', '周二5,6节'),
        ('周二7,8节', '周二7,8节'),
        ('周二9,10节', '周二9,10节'),
        ('周二11,12节', '周二11,12节'),
        ('周三1,2节', '周三1,2节'),
        ('周三3,4节', '周三3,4节'),
        ('周三5,6节', '周三5,6节'),
        ('周三7,8节', '周三7,8节'),
        ('周三9,10节', '周三9,10节'),
        ('周三11,12节', '周三11,12节'),
        ('周四1,2节', '周四1,2节'),
        ('周四3,4节', '周四3,4节'),
        ('周四5,6节', '周四5,6节'),
        ('周四7,8节', '周四7,8节'),
        ('周四9,10节', '周四9,10节'),
        ('周四11,12节', '周四11,12节'),
        ('周五1,2节', '周五1,2节'),
        ('周五3,4节', '周五3,4节'),
        ('周五5,6节', '周五5,6节'),
        ('周五7,8节', '周五7,8节'),
        ('周五9,10节', '周五9,10节'),
        ('周五11,12节', '周五11,12节'),
    )
    course_name = forms.CharField(label="课程名称",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '课程名称...'}))
    #teacher_name = forms.CharField(label="开课教师",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课教师...'}))
    course_time = forms.ChoiceField(label="开课时间",choices=time)
    course_locus = forms.ChoiceField(label="开课地点",choices=locus)
    course_credit = forms.CharField(label="学分",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '学分...'}))
    course_introduction = forms.CharField(label="简介",max_length=128,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '简介...'}))
    course_deadline = forms.CharField(label="选课截止日期", widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': '作业截止日期 格式如：2019-04-12 15:15:15'}))

class UpdateForm(forms.Form):

    number = forms.CharField(label='学号/工号', max_length=50, required=False)
    tel = forms.CharField(label='电话', max_length=50, required=False)
    email = forms.CharField(label='邮箱', max_length=50, required=False)
    addr = forms.CharField(label='地址', max_length=50, required=False)



class CourseUpdateForm(forms.Form):
    locus = (
        ('(一)101', '(一）101'),
        ('(一)102', '(一）102'),
        ('(一)103', '(一）103'),
        ('(一)104', '(一）104'),
        ('(一)201', '(一）201'),
        ('(一)202', '(一）202'),
        ('(一)203', '(一）203'),
        ('(一)204', '(一）204'),
        ('(一)301', '(一）301'),
        ('(一)302', '(一）302'),
        ('(一)303', '(一）303'),
        ('(一)304', '(一）304'),
        ('(二)101', '(二）101'),
        ('(二)102', '(二）102'),
        ('(二)103', '(二）103'),
        ('(二)104', '(二）104'),
        ('(二)201', '(二）201'),
        ('(二)202', '(二）202'),
        ('(二)203', '(二）203'),
        ('(二)204', '(二）204'),
        ('(二)301', '(二）301'),
        ('(二)302', '(二）302'),
        ('(二)303', '(二）303'),
        ('(二)304', '(二）304'),
        ('(三)101', '(三）101'),
        ('(三)102', '(三）102'),
        ('(三)103', '(三）103'),
        ('(三)104', '(三）104'),
        ('(三)201', '(三）201'),
        ('(三)202', '(三）202'),
        ('(三)203', '(三）203'),
        ('(三)204', '(三）204'),
        ('(三)301', '(三）301'),
        ('(三)302', '(三）302'),
        ('(三)303', '(三）303'),
        ('(三)304', '(三）304'),
    )
    time = (
        ('周一1,2节', '周一1,2节'),
        ('周一3,4节', '周一3,4节'),
        ('周一5,6节', '周一5,6节'),
        ('周一7,8节', '周一7,8节'),
        ('周一9,10节', '周一9,10节'),
        ('周一11,12节', '周一11,12节'),
        ('周二1,2节', '周二1,2节'),
        ('周二3,4节', '周二3,4节'),
        ('周二5,6节', '周二5,6节'),
        ('周二7,8节', '周二7,8节'),
        ('周二9,10节', '周二9,10节'),
        ('周二11,12节', '周二11,12节'),
        ('周三1,2节', '周三1,2节'),
        ('周三3,4节', '周三3,4节'),
        ('周三5,6节', '周三5,6节'),
        ('周三7,8节', '周三7,8节'),
        ('周三9,10节', '周三9,10节'),
        ('周三11,12节', '周三11,12节'),
        ('周四1,2节', '周四1,2节'),
        ('周四3,4节', '周四3,4节'),
        ('周四5,6节', '周四5,6节'),
        ('周四7,8节', '周四7,8节'),
        ('周四9,10节', '周四9,10节'),
        ('周四11,12节', '周四11,12节'),
        ('周五1,2节', '周五1,2节'),
        ('周五3,4节', '周五3,4节'),
        ('周五5,6节', '周五5,6节'),
        ('周五7,8节', '周五7,8节'),
        ('周五9,10节', '周五9,10节'),
        ('周五11,12节', '周五11,12节'),
    )
    course_name = forms.CharField(label='课程名称', max_length=50, required=False)
    teacher_name = forms.CharField(label='开课教师', max_length=50, required=False)
    course_time = forms.ChoiceField(label='开课时间', choices=time, required=False)
    course_locus = forms.ChoiceField(label='开课地点', choices=locus, required=False)
    course_credit = forms.CharField(label='学分', max_length=50, required=False)
    course_introduction = forms.CharField(label='简介', max_length=128, required=False)
    course_deadline = forms.CharField(label='选课截止日期', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': '作业截止日期 格式如：2019-04-12 15:15:15'}), required=False)

class AssignForm(forms.ModelForm):
    name = forms.CharField(
        label="作业标题",max_length = 64,
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '作业标题'}
            ),
        )
    content = forms.CharField(
        label="作业详细内容",max_length = 1024,
        widget=forms.Textarea(
            attrs={'rows': 5,'placeholder': '作业详细内容'}
            ),
        )
    deadline = forms.CharField(
         label="截止日期",
         widget=forms.DateTimeInput(
            attrs={'class': 'form-control','placeholder': '作业截止日期 格式如：2019-04-12 15:15:15'}
            ),
     )

    class Meta:
        model = Homework
        fields = ['name', 'content','deadline' ]

class SubmitForm(forms.ModelForm):
    submit = forms.CharField(
        label="提交内容",max_length=1024,
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '输入提交内容'}
            )

        )
    myfile = forms.FileField(
        label="上传文件",
        widget=forms.FileInput(
            #attrs={'class': 'form-control', 'placeholder': '上传文件'}
        )
    )
    class Meta:
        model = SubmitWork
        fields = ['submit' ,'myfile']

class ResourceForm(forms.ModelForm):
    name = forms.CharField(
        label="资源题目",max_length=1024,
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '输入所上传资源的题目'}
            )

        )
    myfile = forms.FileField(
        label="上传文件",
        widget=forms.FileInput(
            #attrs={'class': 'form-control', 'placeholder': '上传文件'}
        )
    )
    class Meta:
        model = Resource
        fields = ['name' ,'myfile']

class GradeForm(forms.ModelForm):
    grade = forms.CharField(label='请打分', max_length=50)

    class Meta:
        model = SubmitWork
        fields = ['grade' ]
