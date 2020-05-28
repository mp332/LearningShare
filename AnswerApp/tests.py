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
        """
            测试用户点赞功能
        """
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
        """
            测试答案收藏功能
        """
        category, question, answer, author = create_category_question_answer()
        collect_answer = AnswerModel.objects.get(id=answer.id)
        self.assertIs(collect_answer.grade, 0)
        # 检查初始答案的热度是否为0
        url = reverse('answer:collect', args=(answer.id,))
        self.client.force_login(author)
        self.client.get(url)
        collect_answer = AnswerModel.objects.get(id=answer.id)
        self.assertIs(collect_answer.grade, 2)
        self.assertIs((author in collect_answer.collect.all()), True)
        # 检查collect_answer中是否有收藏者author
        self.assertIs((collect_answer in author.collect_answer.all()), True)
        # 检查collect_answer中是否在author收藏的答案中

        # 测试重复收藏无效功能
        response = self.client.get(url)
        collect_answer2 = AnswerModel.objects.get(id=answer.id)
        self.assertIs(collect_answer2.grade, 2)
        self.assertContains(response, '您已收藏过')

    def test_delete_answer(self):
        category, question, answer, author = create_category_question_answer()
        guest = User.objects.create(username='user2', password='test_password')
        answer_delete = AnswerModel.objects.get(id=answer.id)
        url = reverse('answer:answer_delete', args=(answer.id,))

        # 检查非作者不能删除答案功能
        self.client.force_login(guest)
        self.client.get(url)
        self.assertEqual(AnswerModel.objects.get(id=answer.id), answer_delete)
        # 检查该问题是否被删除

        # 检查作者删除答案功能
        self.client.force_login(author)
        self.client.get(url)
        self.assertEqual((AnswerModel.objects.filter(id=answer.id)).count(), 0)

        # 检查删除不存在问题
        response = self.client.get(url)
        self.assertContains(response, '该答案不存在')

    def test_author_change_answer(self):
        """
            测试删除答案是否正常
        """
        category, question, answer, author = create_category_question_answer()
        self.client.force_login(author)
        url = reverse('answer:answer_change', args=(answer.id,))
        self.client.post(url, {'question': question, 'editormd-markdown-doc': 'change-answer'})
        answer_change = AnswerModel.objects.get(id=answer.id)
        self.assertEqual(answer_change.answer_text, 'change-answer')

    def test_guest_change_answer(self):
        """
            测试非回答者不能更改答案
        """
        category, question, answer, author = create_category_question_answer()
        guest = User.objects.create(username='user2', password='test_password')
        self.client.force_login(guest)
        url = reverse('answer:answer_change', args=(answer.id,))
        response = self.client.post(url, {'question': question, 'editormd-markdown-doc': 'guest-try'})
        guest_change_answer = AnswerModel.objects.get(id=answer.id)
        self.assertEqual(guest_change_answer.answer_text, 'test')
        self.assertContains(response, '对不起，您没有权限')
