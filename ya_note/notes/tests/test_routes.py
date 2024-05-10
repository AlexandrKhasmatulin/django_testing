from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пётр')
        cls.another_author = User.objects.create(username='Павел')
        cls.note = Note.objects.create(title='Заголовок',
                                       author=cls.author,
                                       slug='slug-text',
                                       text='Текст заметки')

    def test_pages_for_auth_user(self):
        urls = (
            '/add/',
            '/notes/',
            '/done/',
        )
        self.client.force_login(self.author)
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_note_edit_delete_for_author_only(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.another_author, HTTPStatus.NOT_FOUND),
        )
        urls = (
            '/edit/slug-text/',
            '/note/slug-text/',
            '/delete/slug-text/',
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in urls:
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_home_and_auth_pages_for_anonymous_user(self):
        urls = (
            '/',
            '/auth/login/',
            '/auth/signup/',
            '/auth/logout/',
        )
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_redirect(self):
        login_url = '/auth/login/'  # Explicit login URL
        urls = (
            '/add/',
            '/notes/',
            '/done/',
            f'/edit/{self.note.slug}/',
            f'/note/{self.note.slug}/',
            f'/delete/{self.note.slug}/',
        )

        for url in urls:
            redirect_url = f'{login_url}?next={url}'
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
