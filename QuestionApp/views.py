from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from .forms import AskForm
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from AnswerApp.models import AnswerModel


# Create your views here.


def index(request):
    # print(request.GET)
    category_id = request.GET.get('category_id')
    # print(category_id)

    if len(request.GET) == 0:
        question_1 = Question.objects.all().order_by('-goodNum', 'created', 'questionTitle')
        question_2 = Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]
    else:
        question_1 = Question.objects.filter(questionCategory_id=category_id).order_by('-goodNum', 'created', 'questionTitle')
        question_2 = Question.objects.filter(questionCategory_id=category_id).order_by('-views', 'created',
                                                                                       'questionTitle')
    categorys = Category.objects.all()
    context = {
        "question_1": question_1,
        "question_2": question_2,
        "categorys": categorys
    }

    return render(request, "index.html", context=context)


def question_content(request, question_id):
    question = Question.objects.get(id=question_id)
    question.views=question.views+1
    question.save()
    answer_list = AnswerModel.objects.filter(question_id=question_id)
    questions = Question.objects.all()
    context = {
        "question": question,
        "answer_list": answer_list,
        "questions": questions
    }
    
    return render(request, "question/content.html", context=context)


@login_required(login_url='/account/login')
#@csrf_exempt
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
        #print(user)
        #print(request.POST)
        if form.is_valid():
            question_category_number = request.POST.get('category')
            question_title = request.POST.get('title')
            question_text = request.POST.get('editormd-markdown-doc')
            question_category = Category.objects.get(number=question_category_number)
            question = Question(
                user=user,
                questionTitle=question_title,
                questionCategory=question_category,
                questionDescription=question_text,
            )
            question.save()
            # return HttpResponseRedirect(reverse('question_and_answer:detail', args=(question.id,)))
            return HttpResponse("添加成功")
        else:
            context['askMessage'] = "您的输入含有非法字符, 请重试!"
            form = AskForm()
            return HttpResponse("问题添加失败")
    else:
            form = AskForm()
            category = Category.objects.all()
            questions = Question.objects.all()
            return render(request, 'question/add_question.html', {"category": category, "form": form, "questions": questions})


@csrf_exempt
#@require_POST
@login_required(login_url='/account/login')
def like_question(request,id,action):
    #question_id = request.POST.get("id")
    #action = request.POST.get("action")

    #print(request)
    if id and action:
        try:
            question = Question.objects.get(id=id)
            if action == "like":
                question.users_like.add(request.user)
                question.goodNum = question.goodNum+1
                question.save()
                return HttpResponse("点赞成功")
            else:
                question.users_like.remove(request.user)
                question.badNum = question.badNum+1
                question.save()
                return HttpResponse("踩成功")
        except:
            return HttpResponse("no")
    else:
        return HttpResponse("操作失败")


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

    #按照赞数、时间、名称进行排序
    question_list = Question.objects.filter(questionTitle__icontains=keyword).order_by('-goodNum', 'created', 'questionTitle')
    #按照发布时间、问题进行排序
    answer_list = AnswerModel.objects.filter(answer_text__icontains=keyword).order_by('-pub_date', 'question')
    #按照用户名进行排序
    user_list = User.objects.filter(username__icontains=keyword).order_by('-username')
    print(user_list)
    print(question_list)
    print(answer_list)
    questions = Question.objects.all()
    return render(request, 'question/search.html', {'err_msg': err_msg, 'question_list': question_list,
                                                    'answer_list': answer_list, 'user_list': user_list,
                                                    'keyword': keyword, 'questions': questions})



def questionContent(request):
    id = request.GET.get('user')
    username = User.objects.get(id=id)
    question_list = Question.objects.filter(user=id)
    questions = Question.objects.all()
    return render(request, 'question/show_question.html', {'username':username, 'question_list':question_list, "questions": questions})

@csrf_exempt
#@require_POST
@login_required(login_url='/account/login')
def collect(request,id,action):
    # question_id = request.POST.get("id")
    # action = request.POST.get("action")

    # print(request)
    if id and action:
        try:
            question = Question.objects.get(id=id)
            if action == "收藏":
                question.collect.add(request.user)
                question.grade = question.grade+20
                question.save()
                return HttpResponse("收藏成功")
            else:
                question.collect.remove(request.user)
                question.grade = question.grade-20
                question.save()
                return HttpResponse("取消收藏成功")
        except:
            return HttpResponse("no")
    else:
        return HttpResponse("操作失败")


def my_questions(request):
    username = request.user.username
    is_logged_in = True
    context = {
        'username': username,
        'is_logged_in': is_logged_in,
    }
    questions = request.user.questions.all()
    answers = request.user.answers.all()
    context['questions'] = questions
    context['answers'] = answers
    return render(request, 'question/my_questions.html', context)


@login_required(login_url='/account/login')
@csrf_exempt
def redit_question(request,question_id):
    if request.method == "GET":
        question = Question.objects.get(id=question_id)

        question_form = AskForm(initial={"title": question.questionTitle, "category": question.questionCategory})
        return render(request, 'question/redit_question.html', {"question":question, "question_form": question_form})
    else:
        redit_question = Question.objects.get(id=question_id)
        try:
            redit_question.questionTitle = request.POST['title']
            redit_question.questionDescription = request.POST['editormd-markdown-doc']
            redit_question.save()
            return HttpResponse("修改成功")
        except:
            print(request)
            return HttpResponse("修改失败")


def my_collections(request):
    pass

