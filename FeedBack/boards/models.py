from django.db import models

# Create your models here.
from login.models import User,course

class Board(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)
	course = models.ForeignKey(course, related_name='board', on_delete=models.CASCADE)
	def __str__(self):
		return self.name

	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):

		return Post.objects.filter(topic__board=self).order_by('-created_at').first()

	class Meta:
		#ordering = ['c_time']
		verbose_name = '反馈区'
		verbose_name_plural = '反馈区'

class Topic(models.Model):
	subject = models.CharField(max_length=255)
	kind = models.CharField(max_length=128,default='讨论&提问')
	topictype = models.CharField(max_length=64,null=True,default="")
	# time is confrimed when created
	last_updated = models.DateTimeField(auto_now_add=True)
	#use Board.topics to visit Topic
	board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
	starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
	views = models.PositiveIntegerField(default=0)#record page views
	message = models.TextField(max_length=4000)
	def __str__(self):
		return self.subject

	class Meta:
		#ordering = ['c_time']
		verbose_name = '课程反馈区'
		verbose_name_plural = '课程反馈区'

class Post(models.Model):
	message = models.TextField(max_length=4000)
	kind = models.CharField(max_length=128,default='讨论&提问')
	#type of post
	posttype = models.CharField(max_length=64,null=True,default="")
	topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
	#no reverse needed
	updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.CASCADE)

	def __str__(self):
		return self.message

	class Meta:
		#ordering = ['c_time']
		verbose_name = '帖子'
		verbose_name_plural = '帖子'
