from django.shortcuts import render,get_object_or_404,redirect
from login.models import course,User,Homework,SubmitWork,Resource
from .forms import UserForm
from .forms import RegisterForm

from .forms import CreateCourseForm,CourseUpdateForm
from .forms import UpdateForm,AssignForm,SubmitForm,GradeForm,ResourceForm

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
    time = datetime.datetime.now()
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)
    return render(request,'login/index.html',{"course_list":course_list,"time":time,"u":user})

def assistant(request,pk):
    user_list=User.objects.all()
    course_pk = get_object_or_404(course, pk=pk)
    return render(request, 'login/assistant.html', {"user_list": user_list,"course":course_pk})

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
        return render(request, 'login/logout.html', locals())
    request.session.flush()
    return render(request, 'login/logout.html', locals())

def Download(request,path):
    return redirect("/media/"+path)



def CreateCourse(request):
    legal=1
    if request.method=="POST":
        CreateCourse_form = CreateCourseForm(request.POST)
        if CreateCourse_form.is_valid():
            course_name = CreateCourse_form.cleaned_data['course_name']
            teacher_name = CreateCourse_form.cleaned_data['teacher_name']
            course_time = CreateCourse_form.cleaned_data['course_time']
            course_locus = CreateCourse_form.cleaned_data['course_locus']
            course_credit = CreateCourse_form.cleaned_data['course_credit']
            course_introduction = CreateCourse_form.cleaned_data['course_introduction']
            course_deadline = CreateCourse_form.cleaned_data['course_deadline']
            try:
                course_before= course.objects.get(course_locus=course_locus, course_time=course_time)
                legal=0
            except course.DoesNotExist:
                print('error')
            if legal==0:
                message = "已存在另一课程设在此时间与地点！"
            else:
                new_course = models.course.objects.create()
                new_course.course_name = course_name
                new_course.teacher_name = teacher_name
                new_course.course_time = course_time
                new_course.course_locus = course_locus
                new_course.course_credit = course_credit
                new_course.course_introduction = course_introduction
                new_course.course_deadline = course_deadline
                new_course.save()
                print("99999999",new_course.board)
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
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)

    return render(request, 'login/courses.html', {'course': course_pk,'user':user})


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


def course_update(request,pk):
    course_pk = get_object_or_404(course, pk=pk)
    if request.method == "POST":
        form = CourseUpdateForm(request.POST)

        if form.is_valid():
            course_pk.course_name = form.cleaned_data['course_name']
            course_pk.teacher_name = form.cleaned_data['teacher_name']
            course_pk.course_time = form.cleaned_data['course_time']
            course_pk.course_locus = form.cleaned_data['course_locus']
            course_pk.course_credit = form.cleaned_data['course_credit']
            course_pk.course_introduction = form.cleaned_data['course_introduction']
            course_pk.course_deadline = form.cleaned_data['course_deadline']
            course_pk.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        default_data = {'course_name': course_pk.course_name, 'teacher_name': course_pk.teacher_name,'course_time': course_pk.course_time, 'course_locus': course_pk.course_locus,'course_credit': course_pk.course_credit,'course_introduction': course_pk.course_introduction,'course_deadline': course_pk.course_deadline}
        form = CourseUpdateForm(default_data)

    return render(request, 'login/course_update.html', {'form':form, 'course': course_pk})

def choose_course(request,pk):
    new_course= get_object_or_404(course, pk=pk)
    user = User.objects.get(name=request.session.get('user_name'))
    user.courses.add(new_course)
    course_list = course.objects.all()
    choose_courses=user.courses.all()
    print(choose_courses)
    #return render(request, 'login/index.html',{'course_list':course_list},{'choose_courses':choose_courses})
    return redirect('index')

def delete_student(request,course_pk,user_pk):
    course_now= get_object_or_404(course, pk=course_pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses.remove(course_now)
    return render(request, 'login/courses.html',{'course':course_now})

#删除专职助教
def delete_assistant(request,course_pk,user_pk):
    course_now= get_object_or_404(course, pk=course_pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses.remove(course_now)
    models.Privilege.objects.get(course=course_now,user=user_now).delete()
    return render(request, 'login/courses.html',{'course':course_now})

#删除学生助教
def delete_stu_assistant(request,course_pk,user_pk):
    course_now= get_object_or_404(course, pk=course_pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses_1.remove(course_now)
    models.Privilege.objects.get(course=course_now, user=user_now).delete()
    return render(request, 'login/courses.html',{'course':course_now})

#老师为某个课程选择专职助教
def assistant_select(request,pk,user_pk):
    flag = 1
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses.add(course_now)
    for i in models.Privilege.objects.all():
        if i.course == course_now:
            if i.user == user_now:
                flag = 0
    if flag == 1:
        models.Privilege.objects.create(privilege_1='0',privilege_2='0',privilege_3='0',privilege_4='0',privilege_5='0',course=course_now,user=user_now)
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

#老师为某个课程选择学生助教
def stu_assistant_select(request,pk,user_pk):
    flag = 1
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    user_now.courses_1.add(course_now)
    for i in models.Privilege.objects.all():
        if i.course == course_now:
            if i.user == user_now:
                flag = 0
    if flag == 1:
        models.Privilege.objects.create(privilege_1='0', privilege_2='0', privilege_3='0', privilege_4='0', privilege_5='0',course=course_now, user=user_now)
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

def search(request,pk):
    flag = 0
    course_now = get_object_or_404(course, pk=pk)
    q=request.GET.get('q')
    for u in User.objects.all():
        if u.name == q:
            flag = 1
    if flag == 1:
        user = User.objects.get(name=q)
        if user.identity == "student":
            if user in course_now.users.all():
                flag = 2
    if flag == 1:
        user = User.objects.get(name=q)
    else:
        user = get_object_or_404(User, pk=1)
    return render(request,'login/search_select.html',{'course':course_now,'user':user,'flag':flag})


def search_select(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    return render(request, 'login/search_select.html', {'course': course_now, 'user': user_now})

#赋予特权1
def pri_grade(request,pk,user_pk):
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_1 = 1
            i.save()
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

#取消特权1
def cancel_pri1(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_1 = 0
            i.save()
    return redirect( 'assistant_select',pk=pk,user_pk=user_pk)

#取消特权2
def cancel_pri2(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_2 = 0
            i.save()
    return redirect( 'assistant_select',pk=pk,user_pk=user_pk)

#取消特权3
def cancel_pri3(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_3 = 0
            i.save()
    return redirect( 'assistant_select',pk=pk,user_pk=user_pk)

#取消特权4
def cancel_pri4(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_4 = 0
            i.save()
    return redirect( 'assistant_select',pk=pk,user_pk=user_pk)

#取消特权5
def cancel_pri5(request,pk,user_pk):
    course_now = get_object_or_404(course, pk=pk)
    user_now = get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_5 = 0
            i.save()
    return redirect( 'assistant_select',pk=pk,user_pk=user_pk)

#赋予特权2
def pri_update(request,pk,user_pk):
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_2 = 1
            i.save()
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request,'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

#赋予特权3
def pri_assign(request,pk,user_pk):
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_3 = 1
            i.save()
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

#赋予特权4
def pri_delete(request,pk,user_pk):
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_4 = 1
            i.save()
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

#赋予特权5
def pri_resource(request,pk,user_pk):
    course_now= get_object_or_404(course, pk=pk)
    user_now=get_object_or_404(User, pk=user_pk)
    for i in user_now.user_pri.all():
        if i.course == course_now:
            i.privilege_5 = 1
            i.save()
    Pri = models.Privilege.objects.get(course=course_now, user=user_now)
    return render(request, 'login/privilege.html',{'course':course_now,'user':user_now,'pri':Pri})

def drop_course(request,course_pk,user_pk):
    course_now = get_object_or_404(course, pk=course_pk)
    user_now = get_object_or_404(User, pk=user_pk)
    user_now.courses.remove(course_now)
    return render(request, 'login/personal_center.html', {'user': user_now})

def delete_course(request, course_pk,user_pk):
    course_now = get_object_or_404(course, pk=course_pk)
    user_now = get_object_or_404(User, pk=user_pk)
    models.course.objects.get(pk=course_pk).delete()
    # Board.objects.get(pk=course_now.board.pk).delete()###
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
            c = datetime.datetime.now()
            d = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
            if d < c:
                message = "deadline不能设置过去的时间"
                return redirect('new_homework', pk=pk)
            else:
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
                        if user.identity == "student":
                            flag = 0
                            for submit in homework.submit.all():
                                if submit.author.name == user.name:
                                    flag = 1

                            if flag == 0:
                                if b>a :
                                    if (b-a).seconds == 86399  :

                                            email_title = '请尽快提交作业——作业提醒'
                                            email_body = '点击此处提交作业http://127.0.0.1:8000/course/'+pk+'/homework/'
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
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)

    return render(request, 'login/homeworklist.html',{'h_course':h_course,'user':user})

def HomeworkContent(request, pk, homework_pk):
    homework = get_object_or_404(Homework, pk=homework_pk)
    homework.save()
    # print(homework.content)
    submit_list = SubmitWork.objects.all()
    time = datetime.datetime.now()
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)
    course = homework.course
    return render(request, 'login/homeworkcon.html', {'homework':homework,'submit_list':submit_list,'time':time,'user':user,'course':course})



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
    course_now = get_object_or_404(course,pk = pk)
    sub =  get_object_or_404(SubmitWork,pk = sub_pk)
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)
    print("111111111110")
    request.session['user_privilege_1'] = user.user_pri.privilege_1
    print("111111111111")
    print(user.privilege_1)
    return render(request,'login/subcon.html',{'sub':sub,'user':user,'course':course_now})

#课程资源列表
def ResourceList(request, pk):
    r_course = get_object_or_404(course, pk=pk)
    resource = r_course.resource.all()
    # print(dir(homework))
    name = request.session['user_name']
    user = get_object_or_404(User, name=name)

    return render(request, 'login/resourcelist.html',{'r_course':r_course,'user':user})

#上传课程资源
def NewResource(request,pk):
    resource_course = get_object_or_404(course, pk=pk)
    user = User.objects.get(name=request.session.get('user_name'))
    print(resource_course.course_name)
    if request.method == "POST":
        print("888")
        form = ResourceForm(request.POST,request.FILES)
        if form.is_valid():

            resource=form.save(commit=False)
            resource.course = resource_course
            print("999")
            resource.save()
            
            return redirect('resource_list',pk=pk)
    else:
        # print("ttt")
        Resource_form = ResourceForm()
    print(models.Resource.objects.all())
    return render(request,'login/new_resource.html',locals())


def GiveGrade(request,pk,homework_pk,sub_pk):
    print('22222222')
    sub=get_object_or_404(SubmitWork, pk=sub_pk)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            temp_sub = form.save(commit=False)
            sub.grade=temp_sub.grade
            sub.save()
            return render(request, 'login/subcon.html', {'sub': sub},{'form':form})
    else:
        form = GradeForm(default_data)
    return render(request, 'login/subcon.html', {'sub': sub},{'form':form})

def ResourceCon(request, pk, resource_pk):
    resource = get_object_or_404(Resource, pk=resource_pk)
    # resource.save()
    return render(request, 'login/ResourceCon.html', {'resource':resource})

def resource_delete(request, pk,resource_pk):
    models.Resource.objects.get(pk=resource_pk).delete()
    return redirect('resource_list', pk=pk)
