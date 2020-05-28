from django.test import TestCase
from .models import *
from QuestionApp.models import Question
from django.urls import reverse
from CategoryApp.models import Category


def create_category_question_answer():
    """
    新建category,question,answer,user
    以便测试
    """
    category_test = Category(
        name='测试',
        number=1
    )
    category_test.save()
    author = User.objects.create(username='user1', password='test_password')
    question = Question(
        user=author,
        questionCategory=category_test,
        questionTitle='Title',
        questionDescription='test_question',
    )
    question.save()
    answer = AnswerModel(
        author=author,
        question=question,
        answer_text='test',
    )
    answer.save()
    return category_test, question, answer, author


class QuestionViewTests(TestCase):
    def test_collect_question(self):
        category, question, answer, author = create_category_question_answer()
        # 数据库初始化
        collect_question = QuestionModel.objects.get(id=question.id)
        self.assertIs(collect_question.grade, 0)
        # 检查初始问题的热度是否为0
        url = reverse('question:collect', args=(question.id,))
        # 获取收藏的网址
        self.client.force_login(author)
        # 登录用户author, 收藏函数有检查用户是否登录，所以这一步是必须的
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的collect函数
        collect_question = QuestionModel.objects.get(id=question.id)
        # 更新collect_answer
        self.assertIs(collect_question.grade, 20)
        # 检查收藏后问题的热度是否为20
        collect_question = QuestionModel.objects.get(id=question.id)
        response = self.client.get(url)
        self.assertIs(collect_question.grade, 20)
        # 检查同一用户重复收藏，热度是否不变

