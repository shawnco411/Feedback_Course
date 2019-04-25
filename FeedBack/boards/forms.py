from django import forms

from .models import Topic,Post,Board

class NewBoardForm(forms.ModelForm):
    name = forms.CharField(label='姓名', max_length=30, required=False)
    description = forms.CharField(label='学号', max_length=50, required=False)
    class Meta:
        model = Board
        fields = ['name', 'description']

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What do you want to post?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]