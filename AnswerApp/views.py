from django.shortcuts import render, get_object_or_404
from .models import AnswerModel
from QuestionApp.models import Question
from .forms import AnswerForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# 该重定向后面只能加硬编码url，不能使用直接命名的url，后面需要用reverse来转换
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login/')
def answer(request, question_id):
    """
    先检测用户是否登录，问题是否存在
    根据请求类型，显示答案，或者编写答案
    """
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        #print(request.GET)
        #answers = AnswerModel.objects.filter(question=question)
        # 找到该问题的所有答案,并按照时间顺序排序
        answer_form = AnswerForm()
        return render(request, "question/answer.html",
                      {'answer_form': answer_form, 'question': question})
        # 显示答案撰写页面
    else:
        author = User.objects.get(id=request.user.id)
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_text = answer_form.cleaned_data['answer_text']
            answer_data = AnswerModel(
                author=author,
                question=question,
                answer_text=answer_text,
            )
            answer_data.save()
            answers = AnswerModel.objects.filter(question=question).order_by("pub_date")
            return render(request, "question/content.html", {"answers": answers, 'answer_form': answer_form,
                                                             'question': question})  # 显示答案撰写页面
        else:
            return HttpResponse("error")


@login_required(login_url='/account/login/')
def answer_list(request):
    answers = AnswerModel.objects.filter(question=request.question)
    question = Question.objects.filter(id=request.question.id)
    return render(request, "question/answer.html", {"answers": answers, "question": question})
