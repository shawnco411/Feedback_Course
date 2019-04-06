from django.shortcuts import render,get_object_or_404,redirect
from login.models import course,User
from .forms import UserForm
from .forms import RegisterForm
from .forms import CreateCourseForm
from .forms import UpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from login import models
from django.contrib import messages
# Create your views here.
def index(request):
    course_list=course.objects.all()

    return render(request,'login/index.html',{"course_list":course_list})


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            identity = register_form.cleaned_data['identity']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.identity = identity
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")

def CreateCourse(request):
    if request.method=="POST":
        CreateCourse_form = CreateCourseForm(request.POST)
        if CreateCourse_form.is_valid():
            course_name = CreateCourse_form.cleaned_data['course_name']
            teacher_name = CreateCourse_form.cleaned_data['teacher_name']
            course_time = CreateCourse_form.cleaned_data['course_time']
            course_locus = CreateCourse_form.cleaned_data['course_locus']
            course_credit = CreateCourse_form.cleaned_data['course_credit']
            course_introduction = CreateCourse_form.cleaned_data['course_introduction']

            new_course = models.course.objects.create()
            new_course.course_name = course_name
            new_course.teacher_name = teacher_name
            new_course.course_time = course_time
            new_course.course_locus = course_locus
            new_course.course_credit = course_credit
            new_course.course_introduction = course_introduction
            new_course.save()
            user = User.objects.get(name=request.session.get('user_name'))
            user.courses.add(new_course)
            return redirect('/index/')

    CreateCourse_form = CreateCourseForm()
    return render(request, 'login/create_course.html', locals())

def Course(request,pk):
    course_pk = get_object_or_404(course, pk=pk)
    return render(request, 'login/courses.html', {'course': course_pk})


#def PersonalCenter(request):
#    user = User.objects.get(name=request.session.get('user_name'))
#    return render(request,'login/personal_center.html',{'user':user})

def PersonalCenter(request):
    user = User.objects.get(name=request.session.get('user_name'))

    return render(request, 'login/personal_center.html', {'user': user})

def Update(request):
    user = User.objects.get(name=request.session.get('user_name'))

    if request.method == "POST":
        form = UpdateForm(request.POST)

        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.number = form.cleaned_data['number']
            user.tel = form.cleaned_data['tel']
            user.email = form.cleaned_data['email']
            user.addr = form.cleaned_data['addr']
            user.save()

            return HttpResponseRedirect(reverse('personal_center'))
    else:
        default_data = {'name': user.name, 'number': user.number,'tel': user.tel, 'email': user.email,'addr':user.addr,}
        form = UpdateForm(default_data)

    return render(request, 'login/update.html', {'form':form, 'user': user})





def choose_course(request,pk):
    new_course= get_object_or_404(course, pk=pk)
    user = User.objects.get(name=request.session.get('user_name'))
    user.courses.add(new_course)
    course_list = course.objects.all()
    choose_courses=user.courses.all()
    print(choose_courses)
    return render(request, 'login/index.html',{'course_list':course_list},{'choose_courses':choose_courses})

