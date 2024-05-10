import pytest

from http import HTTPStatus
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_path', (
        '',
        'auth/login/',
        'auth/logout/',
        'auth/signup/'
    )
)
def test_homepage_available_for_anonymous_user(client, url_path):
    response = client.get(f'/{url_path}')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'user, expected_status', (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('non_author_client'),
             HTTPStatus.NOT_FOUND)
    )
)
def test_edit_delete_for_auth_and_non_auth_users(
        user, expected_status, comment
):
    for url in ('/edit_comment/{id}/', '/delete_comment/{id}/'):
        url = url.format(id=comment.id)
        response = user.get(url)
    assert response.status_code == expected_status


def test_edit_delete_for_anonymous_user_redirect(client, comment):
    login_url = '/auth/login/'
    for url in ('/edit_comment/{id}/', '/delete_comment/{id}/'):
        url = url.format(id=comment.id)
        expected_url = f'{login_url}?next={url}'
        response = client.get(url)
    assertRedirects(response, expected_url)
