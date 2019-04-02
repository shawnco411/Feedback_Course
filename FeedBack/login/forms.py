from django import forms


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
    course_name = forms.CharField(label="课程名称",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    teacher_name = forms.CharField(label="开课教师",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_time = forms.CharField(label="开课时间",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_locus = forms.CharField(label="开课地点",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_credit = forms.CharField(label="学分",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_introduction = forms.CharField(label="简介",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))