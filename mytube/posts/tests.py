from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.test import Client
from PIL import Image


class ProfileTest(TestCase):
    # создание тестового клиента, его авторизация и создание поста от его имени
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.test", password="secret"
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(
            text="testpost",
            author=self.user)

    # существует страница авторизованного пользователя
    def test_profile(self):
        response = self.client.get("/testuser/")
        self.assertEqual(response.status_code, 200)

    # авторизованный пользователь может создать новый пост
    def test_newpost(self):
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200)

    # неавторизованный пользователь не может создать новый пост
    def test_nologpost(self):
        self.client.logout()
        response = self.client.get("/new/")
        self.assertNotEqual(response.status_code, 200)

    # def test_include(self):
    #     # наличие записи на отдельной странице поста
    #     response = self.client.get("/testuser/" + str(self.post.pk) + "/")
    #     self.assertEqual(response.status_code, 200)
    #
    #     # наличие записи в профиле пользователя
    #     response = self.client.get("/testuser/")
    #     self.assertIn(self.post, response.context["page"])
    #
    #     # наличие записи на главной странице
    #     response = self.client.get("")
    #     self.assertIn(self.post, response.context["page"])

    # изменение поста авторизованному пользователю
    def test_edit(self):
        st = "/testuser/" + str(self.post.pk) + "/edit/"
        response = self.client.post(st, {'text': 'was edit'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # наличие записи в профиле пользователя
        response = self.client.get("/testuser/")
        self.assertNotEqual(self.post.text, response.context["page"][0].text)

    # тест создания страницы вывода ошибки
    def test_404(self):
        response = self.client.get("/dfgdfgd/")
        self.assertEqual(response.status_code, 404)


# тест проверки наличия картинки
class ImageTest(TestCase):
    # создание пользователя и поста с картинкой
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.test", password="secret"
        )
        self.client.force_login(self.user)
        img = Image.open('./media/posts/IMG_8589.JPG')
        self.client.post("new", {'text': 'was edit', "image": img}, follow=True)
        self.post = Post.objects.get(text='was edit')

# class CashTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username="testuser", email="test@test.test", password="secret"
#         )
#         self.client.force_login(self.user)
#
#     def test_cash(self):
#         response1 = self.client.get("")
#         self.post = Post.objects.create(
#             text="testpost",
#             author=self.user)
#         response2 = self.client.get("")
#         print(response1.context["page"][0])
#         print()
#         print(response2.context["page"][0])
#         # self.assertEqual(response1.context, response2.context)
