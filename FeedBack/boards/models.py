from django.db import models

# Create your models here.
from login.models import User

class Board(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		#ordering = ['c_time']
		verbose_name = '反馈区'
		verbose_name_plural = '反馈区'

class Topic(models.Model):
	subject = models.CharField(max_length=255)
	# time is confrimed when created
	last_updated = models.DateTimeField(auto_now_add=True)
	#use Board.topics to visit Topic
	board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
	starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		#ordering = ['c_time']
		verbose_name = '课程反馈区'
		verbose_name_plural = '课程反馈区'

class Post(models.Model):
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
	#no reverse needed
	updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		#ordering = ['c_time']
		verbose_name = '帖子'
		verbose_name_plural = '帖子'
