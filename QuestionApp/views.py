# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AskForm
from .models import *
from AnswerApp.models import AnswerModel

# import easygui

global keyword
global question_list
global answer_list
global user_list
keyword = ''


def index(request, page_id):
    category_id = request.GET.get('category_id')

    if len(request.GET) == 0:
        question_1 = Question.objects.all().order_by('-grade', 'created', 'questionTitle')
        question_2 = Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]
    else:
        question_1 = Question.objects.filter(questionCategory_id=category_id).order_by('-grade', 'created',
                                                                                       'questionTitle')
        question_2 = Question.objects.filter(questionCategory_id=category_id).order_by('-views', 'created',
                                                                                       'questionTitle')

    paginator = Paginator(question_1, 10)
    page_of_questions = paginator.page(page_id)

    current_page_num = page_of_questions.number

    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if page_range[-1] <= paginator.num_pages - 2:
        page_range.insert(len(page_range), '...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    categorys = Category.objects.all()
    context = {
        "question_1": question_1,
        "question_2": question_2,
        "categorys": categorys,
        'page_of_questions': page_of_questions,
        'page_range': page_range,
    }

    return render(request, "question/index_question.html", context=context)


def question_content(request, question_id):
    question = Question.objects.get(id=question_id)
    question_2 = Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]
    question.views = question.views + 1
    question.save()
    answer_list = AnswerModel.objects.filter(question_id=question_id)
    questions = Question.objects.all()
    context = {
        "question": question,
        "answer_list": answer_list,
        "questions": questions,
        "question_2": question_2
    }

    return render(request, "question/content.html", context=context)


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
            return HttpResponse("1")

        form = AskForm(request.POST)
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
            # easygui.msgbox(u'添加成功', u'提示')
            return HttpResponseRedirect('question/question_index/1/')
        else:
            context['askMessage'] = "您的输入含有非法字符, 请重试!"
            form = AskForm()
            # easygui.msgbox(u'问题添加失败', u'提示')
            return HttpResponseRedirect('/')
    else:
        form = AskForm()
        category = Category.objects.all()
        questions = Question.objects.all()
        return render(request, 'question/add_question.html',
                      {"category": category, "form": form, "questions": questions,
                       "question_2": Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]})


@csrf_exempt
@login_required(login_url='/account/login')
def like_question(request, id, action):  # 赞踩函数
    if id and action:  # action用于判断是赞还是踩
        question = Question.objects.get(id=id)
        if action == "like":
            if request.user not in question.users_like.all():
                question.users_like.add(request.user)
                if request.user in question.users_unlike.all():  # 若该点赞用户之前点过踩，则将之前的踩去除
                    question.users_unlike.remove(request.user)
                    question.badNum = question.badNum - 1
                    question.grade = question.grade - 10

                question.goodNum = question.goodNum + 1
                question.grade = question.grade + 10
                question.save()
                # easygui.msgbox(msg='点赞成功', title='提示')
                return HttpResponseRedirect(reverse('question:question_content', args=[id]))
            else:
                # easygui.msgbox(msg='点赞成功', title='提示')
                return HttpResponseRedirect(reverse('question:question_content', args=[id]))
        else:
            if request.user not in question.users_unlike.all():

                question.users_unlike.add(request.user)
                if request.user in question.users_like.all():
                    question.users_like.remove(request.user)
                    question.goodNum = question.goodNum - 1
                    question.grade = question.grade - 10
                question.badNum = question.badNum + 1
                question.grade = question.grade - 10
                question.save()
                # easygui.msgbox(u'踩成功', u'提示')
                return HttpResponseRedirect(reverse('question:question_content', args=[id]))
            else:
                # easygui.msgbox(u'您已经反对', u'提示')
                return HttpResponseRedirect(reverse('question:question_content', args=[id]))
    else:

        # easygui.msgbox(u'操作失败', u'提示')
        return HttpResponseRedirect(reverse('question:question_content', args=[id]))


def search(request):
    global keyword
    global question_list

    key = request.GET.get('keyword')
    if key is not None:
        keyword = key
    err_msg = ''

    t = request.GET.get('type')
    type = t

    if not keyword:
        err_msg = '请输入关键词'
        return render(request, 'question/search.html', {'err_msg': err_msg,
                                                        'question_2': Question.objects.all().order_by('-views',
                                                                                                      'created',
                                                                                                      'questionTitle')[
                                                                      :10]})

    # 按照赞数、时间、名称进行排序
    q = Question.objects.filter(questionTitle__icontains=keyword).order_by('-goodNum', 'created', 'questionTitle')
    if q != '':
        question_list = q
    # 按照发布时间、问题进行排序
    a = AnswerModel.objects.filter(answer_text__icontains=keyword).order_by('-pub_date', 'question')
    if a != '':
        answer_list = a
    # 按照用户名进行排序
    u = User.objects.filter(username__icontains=keyword).order_by('-username')
    if u != '':
        user_list = u

    return render(request, 'question/search.html', {'err_msg': err_msg, 'question_list': question_list,
                                                    'answer_list': answer_list, 'user_list': user_list,
                                                    'keyword': keyword, 'type': type,
                                                    'question_2': Question.objects.all().order_by('-views', 'created',
                                                                                                  'questionTitle')[
                                                                  :10]})


def questionContent(request):
    id = request.GET.get('user')
    username = User.objects.get(id=id)
    question_list = Question.objects.filter(user=id)
    questions = Question.objects.all()
    return render(request, 'question/show_question.html',
                  {'username': username, 'question_list': question_list, "questions": questions,
                   'question_2': Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]})


@csrf_exempt
@login_required(login_url='/account/login')
def collect(request, id, action):
    if id and action:
        try:
            question = Question.objects.get(id=id)
            if action == "收藏":
                if request.user in question.collect.all():
                    return HttpResponseRedirect(reverse('question:question_content', args=[id]))
                else:
                    question.collect.add(request.user)
                    question.grade = question.grade + 20
                    question.save()
                    # easygui.msgbox(u'收藏成功', u'提示')
                    return HttpResponseRedirect(reverse('question:question_content', args=[id]))
            else:
                question.collect.remove(request.user)
                question.grade = question.grade - 20
                question.save()
                # easygui.msgbox(u'取消收藏成功', u'提示')
                return HttpResponseRedirect(reverse('question:question_content', args=[id]))
        except:
            # easygui.msgbox(u'no', u'提示')
            return HttpResponseRedirect(reverse('question:question_content', args=[id]))
    else:
        # easygui.msgbox(u'操作失败', u'提示')
        return HttpResponseRedirect(reverse('question:question_content', args=[id]))


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
def redit_question(request, question_id):  # 修改问题
    if request.method == "GET":
        question = Question.objects.get(id=question_id)

        question_form = AskForm(initial={"title": question.questionTitle, "category": question.questionCategory})
        return render(request, 'question/redit_question.html', {"question": question, "question_form": question_form})
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


def delete_question(request, question_id):  # 删除问题
    question_delete = Question.objects.get(id=question_id)
    question_delete.delete()
    return HttpResponseRedirect(reverse('question:my_questions', ))


def my_center(request):
    username = request.user.username
    is_logged_in = True
    context = {
        'username': username,
        'is_logged_in': is_logged_in,
    }
    questions = request.user.questions.all()

    context['questions'] = questions
    return render(request, 'question/my_center.html', context=context)


def my_answers(request):
    username = request.user.username
    is_logged_in = True
    context = {
        'username': username,
        'is_logged_in': is_logged_in,
    }
    answers = request.user.answers.all()
    context['answers'] = answers
    return render(request, 'question/my_answers.html', context=context)
