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

class QuestionViewTests(TestCase):
    def test_like_question(self):
        category, question, answer, author = create_category_question_answer()
        # 数据库初始化

        self.assertIs(question.goodNum, 0)
        # 上述函数检查question.goodNum是否为0, 即新创建的问题赞数是否为0
        self.assertIs(question.badNum, 0)
        # 上述函数检查question.badNum是否为0, 即新创建的问题踩数是否为0

        action = 'like'

        url = reverse('question:like_question', args=(question.id, action,))
        # 获取点赞的网址
        self.client.force_login(author)
        # 登录用户author, 点赞函数有检查用户是否登录，所以这一步是必须的
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的like_question函数
        question = Question.objects.get(id=question.id)
        # 更新question
        self.assertIs(question.goodNum, 1)
        # 检查question赞数是否为1

        question = Question.objects.get(id=question.id)
        response = self.client.get(url)
        self.assertIs(question.goodNum, 1)
        # 检查同一用户重复点赞，赞数是否不变

        action = 'unlike'

        url = reverse('question:like_question', args=(question.id, action,))
        # 获取点赞的网址
        self.client.force_login(author)
        # 登录用户author, 点赞函数有检查用户是否登录，所以这一步是必须的
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的like_question函数
        question = Question.objects.get(id=question.id)
        # 更新question
        self.assertIs(question.badNum, 1)
        # 检查question踩数是否为1
        self.assertIs(question.goodNum, 0)
        #点踩之后先前的赞应被取消，所以赞数又变回0

        question = Question.objects.get(id=question.id)
        response = self.client.get(url)
        self.assertIs(question.badNum, 1)
        # 检查同一用户重复点赞，踩数是否不变
