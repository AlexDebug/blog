from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.posts.models import Post
from django.urls import reverse_lazy
from .views import UserPost


# Create your tests here.
class TestUserPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(username="TestUser", email="Test@test.com", password="test")
        cls.user.save()

        cls.post = Post(title="Test Post", content="test", user=cls.user)
        cls.post.save()

        return cls

    def test_user_post(self):
        c = Client()

        response = c.get(reverse_lazy('users:user_post', args=['1']))


        self.assertEqual(self.user.post_set.all()[0], response.context_data['object_list'][0])
        self.assertEqual(self.user, response.context_data['single_object'])
