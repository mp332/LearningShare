from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AskForm
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    questions = Question.objects.all()
    categorys = Category.objects.all()
    context = {
        "questions": questions,
        "categorys": categorys
    }

    return render(request, "index.html", context=context)


def question_content(request, question_id):
    question = Question.objects.get(id=question_id)

    return render(request, "question/content.html", {"question": question})


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
            question_category_number = form.cleaned_data['category']
            question_title = form.cleaned_data['title']
            question_text = form.cleaned_data['question']
            question_category = Category.objects.get(number=question_category_number)
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

    else:
        form = AskForm()
        context['form'] = form
    return render(request, 'question/add_question.html', context)


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
