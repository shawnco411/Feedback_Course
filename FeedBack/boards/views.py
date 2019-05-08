from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count
from .models import Board, Topic, Post
from login.models import User
from .forms import NewTopicForm,PostForm
from django.core.mail import send_mail
from FeedBack.settings import EMAIL_FROM
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence

import yaml
from keras.models import model_from_yaml
import keras.utils

np.random.seed(1337)  # For Reproducibility
import sys

sys.setrecursionlimit(1000000)

# define parameters
maxlen = 100


string_type = 1
#lstm
def create_dictionaries(model=None,
                        combined=None):
    ''' Function does are number of Jobs:
        1- Creates a word to index mapping
        2- Creates a word to vector mapping
        3- Transforms the Training and Testing Dictionaries

    '''
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        #  freqxiao10->0 所以k+1
        w2indx = {v: k + 1 for k, v in gensim_dict.items()}  # 所有频数超过10的词语的索引,(k->v)=>(v->k)
        w2vec = {word: model[word] for word in w2indx.keys()}  # 所有频数超过10的词语的词向量, (word->model(word))

        def parse_dataset(combined):  # 闭包-->临时使用
            ''' Words become integers
            '''
            data = []
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)  # freqxiao10->0
                data.append(new_txt)
            return data  # word=>index

        combined = parse_dataset(combined)
        combined = sequence.pad_sequences(combined, maxlen=maxlen)  # 每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0
        return w2indx, w2vec, combined
    else:
        print ('No data provided...')


def input_transform(string):
    # keras.backend.clear_session()
    words = jieba.lcut(string)
    words = np.array(words).reshape(1, -1)
    model = Word2Vec.load('/Users/vectord/Development/feedback_course/FeedBack/boards/model/Word2vec_model.pkl')
    _, _, combined = create_dictionaries(model, words)
    return combined


def lstm_predict(string):
    keras.backend.clear_session()
    print ('loading model......')
    with open('/Users/vectord/Development/feedback_course/FeedBack/boards/model/lstm.yml', 'r') as f:
        yaml_string = yaml.load(f)
    model = model_from_yaml(yaml_string)
    # string_type = ""
    print ('loading weights......')
    model.load_weights('/Users/vectord/Development/feedback_course/FeedBack/boards/model/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    data = input_transform(string)
    data.reshape(1, -1)
    # print data
    result = model.predict_classes(data)
    # print result # [[1]]
    if result[0] == 1:
        print (string, ' positive')
        string_type = 1
        print("1111")
        # return 1
    elif result[0] == 0:
        print (string, ' neural')
        string_type = 2
        print("2222")
        # return 2
    else:
        print (string, ' negative')
        string_type = 3
        print("3333")
        # return 3

# Create your views here.
def home(request):

    boards = Board.objects.all()
    user = User.objects.get(name=request.session.get('user_name'))
    return render(request, 'boards/home.html', {'boards': boards,'user':user})



def board_topics(request, pk):

    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
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
            topic.message = form.cleaned_data.get('message')
            topic.save()
            #post = Post.objects.create(
            #   message=form.cleaned_data.get('message'),
            #   topic=topic,
            #   created_by=user
            #)
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
            # post.posttype = string_type
            #lstm
            lstm_predict(post.message)
            if(string_type==1):
                post.posttype = "positive"
            elif(string_type==2):
                post.posttype = "neural"
            else:
                post.posttype = "negative"
            print(string_type)
            print(post.posttype)
            print("4444")
            #end_lstm
            post.save()
            email_title = '你有新回复啦——讨论区'
            email_body = '点击此处查看回复http://127.0.0.1:8000/boards/'+pk+'/topics/'+topic_pk
            email = post.topic.starter.email  # 对方的邮箱
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})

def delete_topic(request, pk,topic_pk):
    Topic.objects.get(pk=topic_pk).delete()
    return redirect('board_topics', pk=pk)

def delete_post(request,pk,topic_pk,post_pk):
    Post.objects.get(pk=post_pk).delete()
    return redirect('topic_posts', pk=pk,topic_pk=topic_pk)

