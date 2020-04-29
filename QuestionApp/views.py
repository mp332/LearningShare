from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from AnswerApp.models import AnswerModel
from .forms import AskForm
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    #print(request.GET)
    category_id = request.GET.get('category_id')
    #print(category_id)

    if len(request.GET)==0:
        questions = Question.objects.all()
    else:
        questions = Question.objects.filter(questionCategory_id=category_id)
    categorys = Category.objects.all()
    context = {
        "questions": questions,
        "categorys": categorys
    }

    return render(request, "index.html", context=context)


def question_content(request, question_id):
    question = Question.objects.get(id=question_id)
    answer_list = AnswerModel.objects.filter(question_id=question_id)
    context = {
        "question": question,
        "answer_list": answer_list
    }
    return render(request, "question/content.html",context=context )

@login_required(login_url='/account/login')
def ask(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    context = {
        'username': username,
        'is_logged_in': is_logged_in,
    }
    if request.method == 'POST':
        id = request.user.id
        user = User.objects.get(id=id)
        if user:
            pass
        else:
            # return HttpResponseRedirect(reverse('question_and_answer:index'))
            return HttpResponse("1")

        form = AskForm(request.POST)

        if form.is_valid():
            question_category = form.cleaned_data['category']
            question_title = form.cleaned_data['title']
            question_text = form.cleaned_data['question']
            question = Question(
                user=user,
                questionTitle=question_title,
                questionCategory=question_category,
                questionDescription=question_text,
            )
            question.save()
            # return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))
            return HttpResponse("问题添加成功")
        else:
            context['askMessage'] = "您的输入含有非法字符, 请重试!"
            form = AskForm()
            print(request.POST)
            return HttpResponse("问题添加失败")
    else:
        form = AskForm()
        #category = Category.objects.all()
        return render(request, 'question/add_question.html', { "form": form})


def like(request, id):
    question = Question.objects.get(id=id)
    question.goodNum += 1
    question.grade = question.grade + 10
    question.save()
    # return HttpResponseRedirect(reverse('question_and_answer:detail', args=(id,)))


def unlike(request, id):
    question = Question.objects.get(id=id)
    question.goodNum += 1
    question.grade = question.grade + 10
    question.save()


def search(request):
    keyword = request.GET.get('keyword')
    err_msg = ''

    if not keyword:
        err_msg = '请输入关键词'
        return render(request, 'question/search.html', {'err_msg': err_msg})

    post_list = Question.objects.filter(questionTitle__icontains=keyword)
    print(post_list)
    return render(request, 'question/search.html', {'err_msg': err_msg, 'post_list': post_list, 'keyword': keyword})