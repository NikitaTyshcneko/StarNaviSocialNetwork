from datetime import timedelta
import pytest
from django.test import TestCase
from social_network_app.models import Post
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework import status
from social_network_app.views import PostViewSet
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import DataError

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestPostModel(TestCase):
    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.test_user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword1'
        )

        self.post1 = Post.objects.create(title='Post 1', body='Body of post 1', author=self.test_user,
                                         create_at=timezone.now())

        self.post2 = Post.objects.create(title='Post 2', body='Body of post 2', author=self.test_user2,
                                         create_at=timezone.now()+timedelta(days=31))

        self.url_api_post = '/api/v1/post/'
        self.factory = APIRequestFactory()

    def test_for_check_authorized(self):
        c = APIClient()
        response = c.get(self.url_api_post)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.test_user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.body, 'Test Body')
        self.assertEqual(post.author, self.test_user)

    def test_create_post_without_body(self):
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            post = Post.objects.create(
                title='Test',
                body='',
                author=self.test_user
            )
            post.full_clean()

    def test_create_post_without_title(self):
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            post = Post.objects.create(
                title='',
                body='Test Body',
                author=self.test_user
            )
            post.full_clean()

    def test_title_length_more_than_100(self):
        with pytest.raises(DataError):
            post = Post.objects.create(
                title='«Дослідження основних команд командного процесора та засобів створення пакетних командних файлів операційної системи MS DOS»',
                body='test',
                author=self.test_user
            )

    def test_get_posts_details_(self):
        request = self.factory.get(self.url_api_post+f'/{self.post2.pk}/')
        force_authenticate(request, user=self.test_user)
        view = PostViewSet.as_view({'get': 'retrieve'})

        response = view(request, pk=self.post2.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_posts_details(self):
        post4 = {'title': 'Post 2', 'body': 'Body of post 2', 'author': 'test_user'}
        request = self.factory.patch(self.url_api_post+f'{self.post1.pk}/',  post4)
        force_authenticate(request, user=self.test_user)

        view = PostViewSet.as_view({'patch': 'update'})

        response = view(request, pk=self.post1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        request = self.factory.delete(self.url_api_post+f'/{self.post1.pk}/')
        force_authenticate(request, user=self.test_user)
        view = PostViewSet.as_view({'delete': 'destroy'})

        response = view(request, pk=self.post1.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
