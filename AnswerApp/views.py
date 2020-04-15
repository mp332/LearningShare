from django.shortcuts import render
from .models import Answer


def answer(request, id):
    """
    先检测用户是否登录
    然后将answer中的user,question,answer_text
    :param request:
    :param id:
    :return:返回一个模板
    """
    pass
    # return render(request, template_name)
# Create your views here.
