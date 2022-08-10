from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client=Client()
        self.user_trump=User.object.create_user(

            username='trump'
            password='somepassword'


        )

post_001 = Post.object.create(

    title='첫번째 포스트입니다.',
    content='hell world',
    author=self.user_trump



)

response=self.client.get('/blog/')
soup=BeautifulSoup(response.content,'html.parser')
self.assertIn(post_001,author.username.upper())

