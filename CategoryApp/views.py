from django.shortcuts import render
from .models import Category
from QuestionApp.models import Question


def category(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_logged_in = True
    else:
        username = '未登录'
        is_logged_in = False
    try:
        question_list = []
        for i in range(4):
            question_list.append(Question.objects.filter(question_category__number=i).order_by('-grade')[:6])
        context = {
            'username': username,
            'question_list1': question_list[0],
            'question_list2': question_list[1],
            'question_list3': question_list[2],
            'question_list4': question_list[3],
            'is_logged_in': is_logged_in,
        }
    except:
        context = {
            'username': username,
            'question_list1': [],
            'question_list2': [],
            'question_list3': [],
            'question_list4': [],
            'is_logged_in': is_logged_in,
        }
    return render(request, "category/category.html", context)
