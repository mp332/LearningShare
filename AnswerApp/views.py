from django.shortcuts import render, get_object_or_404
from .models import *
from QuestionApp.models import Question
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
# 该重定向后面只能加硬编码url，不能使用直接命名的url，后面需要用reverse来转换
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from notifications.signals import notify


@login_required(login_url='/account/login/')
def answer(request, question_id):
    """
    先检测用户是否登录，问题是否存在
    根据请求类型，显示答案，或者编写答案
    """
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        answer_form = AnswerForm()
        return render(request, "question/answer.html",
                      {'answer_form': answer_form, 'question': question,
                       'question_2': Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]})
        # 显示答案撰写页面
    else:
        author = User.objects.get(id=request.user.id)
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_text = request.POST.get('editormd-markdown-doc')
            answer_data = AnswerModel(
                author=author,
                question=question,
                answer_text=answer_text,
            )
            answer_data.save()
            return HttpResponseRedirect(reverse('question:question_content', args=(question.id,)))
        else:
            return HttpResponse("error")


def answer_change(request, answer_id):
    change_answer = AnswerModel.objects.get(id=answer_id)
    question = Question.objects.get(id=change_answer.question.id)
    if request.user.id != change_answer.author.id:
        return HttpResponseRedirect(reverse('question:question_content', args=(change_answer.question.id,)))
    else:
        if request.method == 'GET':
            return render(request, "question/change-answer.html",
                          {"change_answer": change_answer, "question": question,
                           "question_2": Question.objects.all().order_by('-views', 'created', 'questionTitle')[
                                         :10]})  # 需要编写修改答案模板
        else:
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                change_answer.answer_text = request.POST.get('editormd-markdown-doc')
                change_answer.save()
                return HttpResponseRedirect(reverse('question:question_content', args=(change_answer.question.id,)))


@login_required(login_url='/account/login/')  # 以登录为前提
def like(request, answer_id):
    like_answer = AnswerModel.objects.get(id=answer_id)
    if request.user in like_answer.user_like_answer.all():  # 您已点赞，不再重复点赞
        return HttpResponseRedirect(reverse('question:question_content', args=(like_answer.question.id,)))
    else:
        like_answer.user_like_answer.add(request.user)  # 进行点赞，分数加10，赞数加1
        like_answer.grade += 10
        like_answer.goodNum += 1
        if request.user != like_answer.author:  # 向回答所有者发送通知
            notify.send(
                request.user,
                recipient=like_answer.author,
                verb='赞了你的回答',
                target=like_answer,
            )
        like_answer.save()
        return HttpResponseRedirect(reverse('question:question_content', args=(like_answer.question.id,)))


@login_required(login_url='/account/login/')
def unlike(request, answer_id):
    unlike_answer = AnswerModel.objects.get(id=answer_id)
    if request.user in unlike_answer.user_unlike_answer.all():
        return HttpResponseRedirect(reverse('question:question_content', args=(unlike_answer.question.id,)))
    else:
        unlike_answer.user_unlike_answer.add(request.user)
        unlike_answer.badNum += 1
        unlike_answer.grade -= 7
        if request.user != unlike_answer.author:  # 向回答所有者发送通知
            notify.send(
                request.user,
                recipient=unlike_answer.author,
                verb='踩了你的回答',
                target=unlike_answer,
            )
        unlike_answer.save()
        return HttpResponseRedirect(reverse('question:question_content', args=(unlike_answer.question.id,)))


@login_required(login_url='/account/login/')
def collect(request, answer_id):
    collect_answer = AnswerModel.objects.get(id=answer_id)
    if request.user in collect_answer.collect.all():
        return HttpResponseRedirect(reverse('question:question_content', args=(collect_answer.question.id,)))
    else:
        collect_answer.collect.add(request.user)
        collect_answer.grade += 2  # 收藏后分数+2
        collect_answer.save()

        if request.user != collect_answer.author:  # 向回答所有者发送通知
            notify.send(
                request.user,
                recipient=collect_answer.author,
                verb='收藏了你的回答',
                target=collect_answer,
            )
        return HttpResponseRedirect(reverse('question:question_content', args=(collect_answer.question.id,)))


@login_required(login_url='/account/login/')
def comment(request, answer_id):
    comment_answer = get_object_or_404(AnswerModel, id=answer_id)
    if request.method == 'GET':
        comment_form = CommentForm()
        return render(request, "question/comment.html",
                      {"answer": comment_answer, "comment_form": comment_form, "question": comment_answer.question,
                       "question_2": Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]})
    else:
        commenter = User.objects.get(id=request.user.id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            comment_data = Comment(
                commenter=commenter,
                answer=comment_answer,
                comment_text=comment_text
            )
            if request.user != comment_answer.author:
                notify.send(
                    request.user,
                    recipient=comment_answer.author,
                    verb='回复了你',
                    target=comment_answer,
                    action_object=comment_data,
                )
            comment_data.save()
            return HttpResponseRedirect(reverse('question:question_content', args=(comment_answer.question.id,)))


def delete_answer(request, answer_id):
    try:
        answer_delete = AnswerModel.objects.get(id=answer_id)
    except:
        return HttpResponse("该答案不存在")
    if request.user.id != answer_delete.author.id:  # 非自己回答则不可删除
        return HttpResponseRedirect(reverse('question:question_content', args=(answer_delete.question.id,)))
    else:
        answer_delete.delete()
    return HttpResponseRedirect(reverse('question:question_content', args=(answer_delete.question.id,)))


def show_comment(request, answer_id):
    answer = AnswerModel.objects.get(id=answer_id)
    comment_list = Comment.objects.filter(answer=answer_id)
    return render(request, 'question/show_comment.html',
                  {"comment_list": comment_list, "answer_id": answer_id, "answer": answer,
                   "question_2": Question.objects.all().order_by('-views', 'created', 'questionTitle')[:10]})
