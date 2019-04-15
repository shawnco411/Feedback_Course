from django.db import models

# Create your models here.
class course(models.Model):
    course_name = models.CharField(max_length=128, unique=True)
    teacher_name = models.CharField(max_length=128)
    course_time = models.CharField(max_length=128)
    course_locus = models.CharField(max_length=128)
    course_credit = models.CharField(max_length=128)
    course_introduction = models.CharField(max_length=128)

    # roster = models.ManyToManyField(User)
    def _str_(self):
        return self.course_name

    class Meta:
        # ordering = ['c_time']
        verbose_name = '课程'
        verbose_name_plural = '课程'



class User(models.Model):
    '''用户表'''

    #gender=(
    #    ('male','男'),
    #    ('female','女'),
    #)

    idens=(
        ('student','学生'),
        ('teacher','教师'),
        ('assistant','助教'),
    )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    identity = models.CharField(max_length=32,choices = idens,default='学生')
    c_time = models.DateTimeField(auto_now_add = True)
    courses = models.ManyToManyField(course,related_name='users')
    tel = models.CharField(max_length=128)
    addr = models.CharField(max_length=128)
    number = models.CharField(max_length=128)

    def _str_(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Homework(models.Model):
    name = models.CharField(max_length=64)
    content = models.CharField(max_length = 512)
    course = models.ForeignKey(course,related_name='homework',on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    # submit = models.CharField(max_length = 1000,null=True)
    # submit_time = models.DateTimeField(auto_now = True,null=True)
    # student = models.ForeignKey(User,related_name = 'homework_sub',on_delete=models.CASCADE,null=True)
    def _str_(self):
        return self.name

class SubmitWork(models.Model):
    submit = models.CharField(max_length = 1000)
    myfile = models.FileField(upload_to="%Y/%m/%d/")
    submit_time = models.DateTimeField(auto_now = True,null=True)
    homework = models.ForeignKey(Homework,related_name = 'submit',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name = 'homework_sub',on_delete=models.CASCADE)



