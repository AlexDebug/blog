from django.test import TestCase, Client, RequestFactory
from .models import Post, Comment
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .views import ListDetail, like, dislike


# Create your tests here.
class TestDetail(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = {"TestUser":"test"}

        cls.user = User.objects.create_user("TestUser", "Test@test.com", "test")
        cls.post = Post(title="Test Post", content="test", user=cls.user)
        cls.comment = Comment(content="test comment", post=cls.post, user=cls.user)

        cls.user.save()
        cls.post.save()
        cls.comment.save()

        return cls

    def test_client_post_detail(self):
        c = Client()

        response = c.get(reverse_lazy('posts:post_detail', args=['1']))

        self.assertEqual('posts/post.html', response.templates[0].name)
        self.assertEqual(self.post.comment_set.all()[0], response.context_data['object_list'][0])
        self.assertEqual(self.post, response.context_data['single_object'])


class TestLike(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.passwords = {"user1":"test1", "user2":"test2", "user3":"test3", "user4":"test4"}

        cls.user1 = User.objects.create_user(username="TestUser1", email="Test1@test.com", password="test1")
        cls.user2 = User.objects.create_user(username="TestUser2", email="Test2@test.com", password="test2")
        cls.user3 = User.objects.create_user(username="TestUser3", email="Test3@test.com", password="test3")
        cls.user4 = User.objects.create_user(username="TestUser4", email="Test4@test.com", password="test4")
        cls.post = Post(title="Test Post", content="test", user=cls.user1)

        cls.user1.save()
        cls.user2.save()
        cls.user3.save()
        cls.user4.save()
        cls.post.save()

        cls.post.like.add(cls.user2)
        cls.post.dislike.add(cls.user3)

        cls.factory = RequestFactory()

        return cls

    def test_like_for_creator(self):
        c = Client()
    
        c.login(username=self.user1.username, password=self.passwords["user1"])

        response = c.get(reverse_lazy('posts:like', args=['1']))

        self.assertEqual(response.status_code, 404)

    def test_like_for_dislike(self):
        c = Client()
        c.login(username=self.user3.username, password=self.passwords["user3"])

        response = c.get(reverse_lazy('posts:like', args=['1']))

        self.assertEqual(response.status_code, 404)

    def test_like_for_like(self):
        c = Client()
        c.login(username=self.user2.username, password=self.passwords["user2"])

        response = c.get(reverse_lazy('posts:like', args=['1']))

        self.assertNotIn(self.user2, self.post.like.all())

    def test_like_for_none(self):
        c = Client()
        c.login(username=self.user4.username, password=self.passwords["user4"])

        response = c.get(reverse_lazy('posts:like', args=['1']))

        self.assertIn(self.user4, self.post.like.all())


class TestDislike(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.passwords = {"user1":"test1", "user2":"test2", "user3":"test3", "user4":"test4"}

        cls.user1 = User.objects.create_user(username="TestUser1", email="Test1@test.com", password="test1")
        cls.user2 = User.objects.create_user(username="TestUser2", email="Test2@test.com", password="test2")
        cls.user3 = User.objects.create_user(username="TestUser3", email="Test3@test.com", password="test3")
        cls.user4 = User.objects.create_user(username="TestUser4", email="Test4@test.com", password="test4")
        cls.post = Post(title="Test Post", content="test", user=cls.user1)

        cls.user1.save()
        cls.user2.save()
        cls.user3.save()
        cls.user4.save()
        cls.post.save()

        cls.post.like.add(cls.user2)
        cls.post.dislike.add(cls.user3)

        cls.factory = RequestFactory()

        return cls

    def test_like_for_creator(self):
        c = Client()
        c.login(username=self.user1.username, password=self.passwords["user1"])

        response = c.get(reverse_lazy("posts:dislike", args=["1"]))
        self.assertEqual(response.status_code, 403)

    def test_like_for_dislike(self):
        c = Client()
        c.login(username=self.user2.username, password=self.passwords["user2"])

        response = c.get(reverse_lazy("posts:dislike", args=["1"]))

        self.assertEqual(response.status_code, 403)

    def test_like_for_like(self):
        c = Client()
        c.login(username=self.user3.username, password=self.passwords["user3"])

        response = c.get("/blog/1/dislike/")
        self.assertIn(self.user3, self.post.dislike.all())

    def test_like_for_none(self):
        c = Client()
        c.login(username=self.user4.username, password=self.passwords["user4"])

        response = c.get(reverse_lazy("posts:dislike", args=["1"]))
        print(response)
        self.assertIn(self.user4, self.post.dislike.all())
