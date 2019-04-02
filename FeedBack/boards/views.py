from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post
from login.models import User

# Create your views here.
def home(request):

	boards = Board.objects.all()
	return render(request, 'boards/home.html', {'boards': boards})



def board_topics(request, pk):

	board = get_object_or_404(Board, pk=pk)
	return render(request, 'boards/topics.html', {'board': board})



def new_topic(request, pk):

	board = get_object_or_404(Board, pk=pk)
	return render(request, 'boards/new_topic.html', {'board': board})


def new_topic(request, pk):

	board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':
		subject = request.POST['subject']
		message = request.POST['message']

		user = User.objects.first()#临时使⽤⼀个账号作为登录⽤户,可更改为admin定义的

		topic = Topic.objects.create(
			subject=subject,
			board=board,
			starter=user
		)

		post = Post.objects.create(
			message=message,
			topic=topic,
			created_by=user
)

		return redirect('board_topics', pk=board.pk)# TODO:redirect to the created topic page

	return render(request, 'boards/new_topic.html', {'board': board}

)