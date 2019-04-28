from django.db import models

# Create your models here.
class course(models.Model):
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
    course_name = models.CharField(max_length=128)
    teacher_name = models.CharField(max_length=128)
    course_time = models.CharField(max_length=128,choices = time,default='周一1,2节')
    course_locus = models.CharField(max_length=128,choices = locus,default='(一)101')
    course_credit = models.CharField(max_length=128)
    course_introduction = models.CharField(max_length=128)
    course_deadline = models.DateTimeField(default='2019-04-30 12:00:00')
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
    grade = models.CharField(max_length=64,default='未评阅')
    myfile = models.FileField(upload_to="%Y/%m/%d/")
    submit_time = models.DateTimeField(auto_now = True,null=True)
    homework = models.ForeignKey(Homework,related_name = 'submit',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name = 'homework_sub',on_delete=models.CASCADE)

class Resource(models.Model):
    name = models.CharField(max_length = 100)
    myfile = models.FileField(upload_to="%Y/%m/%d/")
    course = models.ForeignKey(course,related_name='resource',on_delete=models.CASCADE)

    def _str_(self):
        return self.name

