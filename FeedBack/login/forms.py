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
    course_name = forms.CharField(label="课程名称",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '课程名称...'}))
    teacher_name = forms.CharField(label="开课教师",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课教师...'}))
    course_time = forms.CharField(label="开课时间",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课时间...'}))
    course_locus = forms.CharField(label="开课地点",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '开课地点...'}))
    course_credit = forms.CharField(label="学分",max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '学分...'}))
    course_introduction = forms.CharField(label="简介",max_length=128,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': '简介...'}))
    #edited by Zhou Haici

class UpdateForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, required=False)
    number = forms.CharField(label='Number', max_length=50, required=False)
    tel = forms.CharField(label='Tel', max_length=50, required=False)
    email = forms.CharField(label='Email', max_length=50, required=False)
    addr = forms.CharField(label='Addr', max_length=50, required=False)
