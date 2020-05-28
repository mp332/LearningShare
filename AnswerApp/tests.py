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


class AnswerViewTests(TestCase):
    def test_like_answer(self):
        category, question, answer, author = create_category_question_answer()
        # 数据库初始化
        like_answer = AnswerModel.objects.get(id=answer.id)
        self.assertIs(like_answer.goodNum, 0)
        # 上述函数检查like_answer.goodNum是否为0, 即新创建的答案赞数是否为0

        url = reverse('answer:like', args=(answer.id,))
        # 获取点赞的网址
        self.client.force_login(author)
        # 登录用户author, 点赞函数有检查用户是否登录，所以这一步是必须的
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的like函数
        like_answer = AnswerModel.objects.get(id=answer.id)
        # 更新like_answer
        self.assertIs(like_answer.goodNum, 1)
        # 检查like_answer赞数是否为1

        like_answer = AnswerModel.objects.get(id=answer.id)
        response = self.client.get(url)
        self.assertIs(like_answer.goodNum, 1)
        # 检查同一用户重复点赞，赞数是否不变

    def test_collect_answer(self):
        category, question, answer, author = create_category_question_answer()
        # 数据库初始化
        collect_answer = AnswerModel.objects.get(id=answer.id)
        self.assertIs(collect_answer.grade, 0)
        # 检查初始答案的热度是否为0
        url = reverse('answer:collect', args=(answer.id,))
        # 获取收藏的网址
        self.client.force_login(author)
        # 登录用户author, 收藏函数有检查用户是否登录，所以这一步是必须的
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的collect函数
        collect_answer = AnswerModel.objects.get(id=answer.id)
        # 更新collect_answer
        self.assertIs(collect_answer.grade, 2)
        # 检查收藏后答案的热度是否为2

        

    def test_delete_answer(self):
        category, question, answer, author = create_category_question_answer()
        # 数据库初始化
        answer_delete = AnswerModel.objects.get(id=answer.id)
        self.assertEqual(answer_delete.author, answer.author)
        # 检查当前用户是不是回答用户

        url = reverse('answer:answer_delete', args=(answer.id,))
        # 获取删除的网址
        self.client.force_login(author)
        # 登录用户author，删除函数需要用户登录
        response = self.client.get(url)
        # 向url对应的视图发起请求并获得了响应response，即调用了views里面的answer_delete函数
        answer_delete = AnswerModel.objects.filter(id=answer.id)
        # 更新answer_delete
        self.assertIs(answer_delete.count(), 0)
        # 检查该问题是否被删除