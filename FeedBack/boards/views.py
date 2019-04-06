from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count
from .models import Board, Topic, Post
from login.models import User
from .forms import NewTopicForm,PostForm

# Create your views here.
def home(request):

	boards = Board.objects.all()
	return render(request, 'boards/home.html', {'boards': boards})



def board_topics(request, pk):

	board = get_object_or_404(Board, pk=pk)
	topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
	return render(request, 'boards/topics.html', {'board': board,'topics': topics})

def new_topic(request, pk):

	# print(Topic.objects.all())

	if  request.session.get('is_login')!=True:
		return redirect('/login')

	board = get_object_or_404(Board, pk=pk)
	user = User.objects.get(name=request.session.get('user_name'))
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = user
			topic.save()
			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=user
			)
			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()
	return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
	topic = get_object_or_404(Topic, pk=topic_pk)#why can't use board__pk???
	# print(topic.board.pk)
	# print(pk)
	# print(topic.pk)
	# print(topic.subject)
	topic.views+=1
	topic.save()
	return render(request, 'boards/topic_posts.html', {'topic': topic})


def reply_topic(request, pk, topic_pk):
	topic = get_object_or_404(Topic, pk=topic_pk)
	user = User.objects.get(name=request.session.get('user_name'))
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = user
			post.save()
			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
	else:
		form = PostForm()
	return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})
