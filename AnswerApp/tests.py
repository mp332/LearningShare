from django.test import TestCase
from .models import *
from django.urls import reverse
from QuestionApp.models import Question
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


def create_category_question():
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
    return category_test, question, author


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

    def test_unlike_answer(self):
        """
           测试用户踩功能
        """
        category, question, answer, author = create_category_question_answer()  # 数据库初始化
        unlike_answer = AnswerModel.objects.get(id=answer.id)
        self.assertIs(unlike_answer.badNum, 0)  # 上述函数检查unlike_answer.goodNum是否为0, 即新创建的答案踩数是否为0
        url = reverse('answer:unlike', args=(answer.id,))  # 获取踩的网址
        self.client.force_login(author)  # 登录用户author, 踩函数有检查用户是否登录
        response = self.client.get(url)  # 向url对应的视图发起请求并获得了响应response, 即调用了views里面的unlike函数
        unlike_answer = AnswerModel.objects.get(id=answer.id)  # 更新unlike_answer
        self.assertIs(unlike_answer.badNum, 1)  # 检查unlike_answer赞数是否为1

        unlike_answer = AnswerModel.objects.get(id=answer.id)
        response = self.client.get(url)
        self.assertIs(unlike_answer.badNum, 1)  # 检查同一用户重复点赞，赞数是否不变

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

    def test_can_comment(self):
        category, question, answer, author = create_category_question_answer()

        # 登录
        self.client.force_login(author)
        comments = Comment.objects.filter(answer=answer)
        # 判断初始无评论
        self.assertEqual(len(comments), 0)
        url = reverse('answer:answer_comment', args=(answer.id,))
        # 打开评论页面
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        # 评论
        response2 = self.client.post(url, {'comment_text': 'test_comment'})

        # 评论后判断,判断评论是否成功
        comments2 = Comment.objects.filter(answer=answer)
        self.assertEqual(len(comments2), 1)
        comment = comments.first()
        self.assertEqual(comment.comment_text, 'test_comment')

        # 评论后的重定向是否正确
        self.assertEqual(response2.status_code, 302)
        url = reverse('question:question_content', args=(question.id,))
        self.assertEqual(response2.url, url)

    def test_show_comment(self):
        category, question, answer, author = create_category_question_answer()
        # 登录
        self.client.force_login(author)
        comments = Comment.objects.filter(answer=answer)
        url = reverse('answer:show_comment', args=(answer.id,))
        # 查看评论
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_answer(self):
        category, question, author = create_category_question()

        # 登录
        self.client.force_login(author)
        answers = AnswerModel.objects.filter(question=question)
        # 判断初始1回答
        self.assertEqual(len(answers), 0)
        url = reverse('answer:answer_question', args=(question.id,))
        # 打开回答页面
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        # 回答
        response2 = self.client.post(url, {'question': question, 'editormd-markdown-doc': 'text_answer'})

        # 回答后判断,判断回答是否成功
        answer1 = AnswerModel.objects.filter(question=question)
        self.assertEqual(len(answer1), 1)
        answer = answer1.first()
        self.assertEqual(answer.answer_text, 'text_answer')

        # 回答后重定向是否正确
        self.assertEqual(response2.status_code, 302)
        url = reverse('question:question_content', args=(question.id,))
        self.assertEqual(response2.url, url)
