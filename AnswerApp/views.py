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
    user = User.objects.get(id=request.user.id)
    print(user.collect_answer.all())
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        # print(request.GET)
        # answers = AnswerModel.objects.filter(question=question)
        # 找到该问题的所有答案,并按照时间顺序排序
        answer_form = AnswerForm()
        return render(request, "question/answer.html",
                      {'answer_form': answer_form, 'question': question})
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
            answers = AnswerModel.objects.filter(question=question).order_by("pub_date")
            return HttpResponseRedirect(reverse('question:question_content', args=(question.id,)))
        else:
            return HttpResponse("error")


def answer_change(request, answer_id):
    change_answer = AnswerModel.objects.get(id=answer_id)
    question = Question.objects.get(id=change_answer.question.id)
    if request.user.id != change_answer.author.id:
        return HttpResponse("对不起，您没有权限")
    else:
        if request.method == 'GET':
            return render(request, "question/change-answer.html",
                          {"change_answer": change_answer, "question": question})  # 需要编写修改答案模板
        else:
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                change_answer.answer_text = request.POST.get('editormd-markdown-doc')
                change_answer.save()
                return HttpResponseRedirect(reverse('question:question_content', args=(change_answer.question.id,)))

            # @login_required(login_url='/account/login/')


# def answer_list(request):
#     print('1')
#     answers = AnswerModel.objects.filter(question=request.question)
#     question = Question.objects.filter(id=request.question.id)
#     return render(request, "question/answer.html", {"answers": answers, "question": question})


@login_required(login_url='/account/login/')
def like(request, answer_id):
    print(answer_id)
    like_answer = AnswerModel.objects.get(id=answer_id)
    if request.user in like_answer.user_like_answer.all():
        return HttpResponse("您已点赞")
    else:
        like_answer.user_like_answer.add(request.user)
        like_answer.grade += 10
        like_answer.goodNum += 1
        if request.user != like_answer.author:
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
        return HttpResponse("您已踩过")
    else:
        unlike_answer.user_unlike_answer.add(request.user)
        unlike_answer.badNum += 1
        unlike_answer.grade -= 7
        if request.user != unlike_answer.author:
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
        return HttpResponse("您已收藏过")
    else:
        collect_answer.collect.add(request.user)
        collect_answer.save()
        if request.user != collect_answer.author:
            notify.send(
                request.user,
                recipient=collect_answer.author,
                verb='收藏了你的回答',
                target=collect_answer,
            )
        return HttpResponseRedirect(reverse('question:question_content', args=(collect_answer.question.id,)))


@login_required(login_url='/account/login/')
def comment(request, answer_id):
    """
    显示评论的方式暂未确定
    """
    comment_answer = get_object_or_404(AnswerModel, id=answer_id)
    if request.method == 'GET':
        # comments = Comment.objects.filter(answer=comment_answer)
        comment_form = CommentForm()
        return render(request, "question/comment.html",
                      {"answer": comment_answer, "comment_form": comment_form, "question": comment_answer.question})
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
            comments = Comment.objects.filter(answer=comment_answer)
            return HttpResponseRedirect(reverse('question:question_content', args=(comment_answer.question.id,)))


def delete_answer(request, answer_id):
    answer_delete = AnswerModel.objects.get(id=answer_id)
    if request.user.id != answer_delete.author.id:
        return HttpResponse("对不起，您没有权限")
    else:
        answer_delete.delete()
    return HttpResponseRedirect(reverse('question:question_content', args=(answer_delete.question.id,)))


def show_comment(request, answer_id):
    # answer_id = request.GET.get('answer_id')
    answer = AnswerModel.objects.get(id=answer_id)
    comment_list = Comment.objects.filter(answer=answer_id)
    return render(request, 'question/show_comment.html',
                  {"comment_list": comment_list, "answer_id": answer_id, "answer": answer})
