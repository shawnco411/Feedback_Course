from django import forms
from login.models import Homework,SubmitWork


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    idens = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('assistant', '助教'),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    identity = forms.ChoiceField(label='身份', choices=idens)
    #captcha = CaptchaField(label='验证码')

class CreateCourseForm(forms.Form):
    course_name = forms.CharField(label="课程名称",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '课程名称...'}))
    teacher_name = forms.CharField(label="开课教师",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课教师...'}))
    course_time = forms.CharField(label="开课时间",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课时间...'}))
    course_locus = forms.CharField(label="开课地点",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课地点...'}))
    course_credit = forms.CharField(label="学分",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '学分...'}))
    course_introduction = forms.CharField(label="简介",max_length=128,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '简介...'}))
    

class UpdateForm(forms.Form):
    name = forms.CharField(label='姓名', max_length=50, required=False)
    number = forms.CharField(label='学号', max_length=50, required=False)
    tel = forms.CharField(label='电话', max_length=50, required=False)
    email = forms.CharField(label='邮箱', max_length=50, required=False)
    addr = forms.CharField(label='地址', max_length=50, required=False)


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
            attrs={'class': 'form-control','placeholder': '作业截止日期'}
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
    class Meta:
        model = SubmitWork
        fields = ['submit' ]


