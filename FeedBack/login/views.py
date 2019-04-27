from django.shortcuts import render,get_object_or_404,redirect
from login.models import course,User,Homework,SubmitWork
from .forms import UserForm
from .forms import RegisterForm
from .forms import CreateCourseForm
from .forms import UpdateForm,AssignForm,SubmitForm,GradeForm
from boards.models import Board
from django.http import HttpResponseRedirect
from django.urls import reverse
from login import models
from boards import models as boards_models
from django.contrib import messages
from django.core.mail import send_mail
from FeedBack.settings import EMAIL_FROM
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job
# Create your views here.
def index(request):
    course_list=course.objects.all()
    #user = request.se
    #print(request.session['identity'])
    '''
    try:

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(test_job,'cron', day_of_week='mon-sun', hour='16', minute='27', second='10')
        #@register_job(scheduler,"interval",seconds=1)
        def test_job():
            t_now = time.localtime()
            print("0000")
            print(t_now)


        register_events(scheduler)

        scheduler.start()

    except Exception as e:
        print(e)
        # 报错则调度器停止执行
        #scheduler.shutdown()
   
    
    sched = BlockingScheduler()

    @sched.scheduled_job('interval', seconds=3)
    def timed_job():
        print('This job is run every three minutes.')

    print('before the start funciton')
    sched.start()
    print("let us figure out the situation")
    '''
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
                    request.session['user_identity']=user.identity

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

def Download(request,path):
    return redirect("/media/"+path)
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

            board = Board.objects.create(
                name=course_name,
                description=course_introduction,
                course=new_course
            )

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
def GiveGrade(request,pk,homework_pk,sub_pk):
    print('22222222')
    sub=get_object_or_404(SubmitWork, pk=sub_pk)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            sub.grade=grade
            sub.save()
            return render(request, 'login/subcon.html', {'sub': sub},{'form':form})
    else:
        default_data={'grade':sub.grade}
        form = GradeForm(default_data)
    return render(request, 'login/subcon.html', {'sub': sub},{'form':form})
def choose_course(request,pk):
    new_course= get_object_or_404(course, pk=pk)
    user = User.objects.get(name=request.session.get('user_name'))
    user.courses.add(new_course)
    course_list = course.objects.all()
    choose_courses=user.courses.all()
    print(choose_courses)
    return render(request, 'login/index.html',{'course_list':course_list},{'choose_courses':choose_courses})
def delete_student(request,course_pk,user_pk):
    course_now= get_object_or_404(course, pk=course_pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses.remove(course_now)

    return render(request, 'login/courses.html',{'course':course_now})

def drop_course(request,course_pk,user_pk):
    course_now = get_object_or_404(course, pk=course_pk)
    user_now = get_object_or_404(User, pk=user_pk)
    user_now.courses.remove(course_now)
    return render(request, 'login/personal_center.html', {'user': user_now})

def delete_course(request, course_pk,user_pk):
    course_now = get_object_or_404(course, pk=course_pk)
    user_now = get_object_or_404(User, pk=user_pk)
    models.course.objects.get(pk=course_pk).delete()
    return render(request, 'login/personal_center.html', {'user': user_now})

def delete_homework(request, pk,homework_pk):
    models.Homework.objects.get(pk=homework_pk).delete()
    return redirect('homework_list', pk=pk)

def Assign(request,pk):
    homework_course = get_object_or_404(course, pk=pk)
    user = User.objects.get(name=request.session.get('user_name'))
    print(homework_course.course_name)
    #email_title = 'test'
    #email_body = '你该交作业啦！'
    #email = '2749592909@qq.com'  # 对方的邮箱
    #email_from = user.email
    #send_status = send_mail(email_title, email_body, email_from, [email])
    if request.method == "POST":
        print("343434")
        form = AssignForm(request.POST)
        if form.is_valid():

            deadline = form.cleaned_data['deadline']
            name = form.cleaned_data['name']
            #new_homework = models.Homework.objects.create()
            # new_homework.name = name
            # new_homework.content = content
            # new_homework.course = homework_course
            # # new_homework.deadline = deadline
            # new_homework.save()
            homework=form.save(commit=False)
            homework.course = homework_course
            homework.save()
            try:
                sched = BackgroundScheduler()
                @sched.scheduled_job('interval', seconds=1)
                def timed_job():
                    a=datetime.datetime.now()
                    b=datetime.datetime.strptime(deadline,"%Y-%m-%d %H:%M:%S")
                    for user in homework.course.users.all():
                        flag = 0
                        for submit in homework.submit.all():
                            if submit.author.name == user.name:
                                flag = 1
                        if flag == 0:
                            if (b-a).seconds == 0:
                                email_title = '作业提醒'
                                email_body = '请赶快提交作业'
                                email = user.email  # 对方的邮箱
                                send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
                sched.start()
            except Exception as e:
                print(e)
                sched.shutdown()

            return redirect('homework_list',pk=pk)
    else:
        # print("ttt")
        assign_form = AssignForm()
    print(models.Homework.objects.all())
    return render(request,'login/assign.html',locals())

def HomeworkList(request, pk):
    h_course = get_object_or_404(course, pk=pk)
    homework = h_course.homework.all()
    # print(dir(homework))
    return render(request, 'login/homeworklist.html',{'h_course':h_course})

def HomeworkContent(request, pk, homework_pk):
    homework = get_object_or_404(Homework, pk=homework_pk)
    homework.save()
    # print(homework.content)
    submit_list = SubmitWork.objects.all()
    return render(request, 'login/homeworkcon.html', {'homework':homework,'submit_list':submit_list})



def HomeworkSubmit(request, pk, homework_pk):
    homework = get_object_or_404(Homework, pk=homework_pk)
    user = User.objects.get(name=request.session.get('user_name'))
    flag=1
    try:
        submit_before=SubmitWork.objects.get(homework=homework,author=user)
    except SubmitWork.DoesNotExist:
        print('error')
        flag=0
    #print(submit_before)
    print('12121212')
    if request.method == "POST":
        print("343434")
        form = SubmitForm(request.POST,request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.homework = homework
            sub.author = user
            sub.grade='未评阅'
            #submit_before.submit_time=sub.submit_time
            if flag==1:
                submit_before.submit=sub.submit
                submit_before.myfile=sub.myfile
                submit_before.submit_time=sub.submit_time
                submit_before.homework=sub.homework
                submit_before.author=sub.author
                submit_before.grade=sub.grade
                submit_before.save()
            else:
                sub.save()
            print("xxx")
            return redirect('homework_list',pk=pk)
        print("zzz")
    else:
        sub_form = SubmitForm()
        print("yyy")

    return render(request, 'login/submit.html',locals())

def SubmitCon(request,pk,homework_pk,sub_pk):
    sub =  get_object_or_404(SubmitWork,pk = sub_pk)
    return render(request,'login/subcon.html',{'sub':sub})

