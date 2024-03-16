import re

import pytest
from pytest_django.asserts import assertTemplateUsed
from conftest import try_get_url


@pytest.mark.parametrize(
    'url, template', [
        ('', 'blog/index.html'),
        ('posts/0/', 'blog/detail.html'),
        ('posts/1/', 'blog/detail.html'),
        ('posts/2/', 'blog/detail.html'),
        ('category/some-category/', 'blog/category.html'),
        ('pages/about/', 'pages/about.html'),
        ('pages/rules/', 'pages/rules.html'),
    ]
)
def test_page_templates(client, url, template):
    url = f'/{url}' if url else '/'
    response = try_get_url(client, url)
    assertTemplateUsed(response, template, msg_prefix=(
        f'Убедитесь, что для отображения страницы `{url}` '
        f'используется шаблон `{template}`.'
    ))


@pytest.mark.parametrize('post_pk', (0, 1, 2))
def test_post_detail(post_pk, client, posts):
    url = f'/posts/{post_pk}/'
    response = try_get_url(client, url)
    assert response.context is not None, (
        'Убедитесь, что в шаблон страницы с адресом `posts/<int:pk>/` '
        'передаётся словарь контекста.'
    )
    post = next((p for p in posts if p['id'] == post_pk), None)
    assert isinstance(response.context.get('post'), dict), (
        'Убедитесь, что в словарь контекста для страницы '
        '`posts/<int:pk>/` по ключу `post` передаётся непустой словарь.'
    )
    assert post == response.context['post'], (
        'Убедитесь, что в словаре контекста для страницы '
        f'`posts/{post_pk}/` под ключом `post` передаётся словарь '
        f'с `"id": {post_pk}` из списка `posts`.'
    )


def test_post_list(client, posts):
    url = '/'
    response = try_get_url(client, url)
    # Убедитесь, что все специальные символы регулярных выражений
    # в текстах сообщений правильны
    reversed_truncated_post_texts = [
        re.escape(post['text'][:20]) for post in reversed(posts)
    ]
    # Создайте шаблон, который допускает любые символы (\s\S)
    # между усеченными текстами сообщений
    reversed_post_list_pattern = re.compile(
        r'[\s\S]+?'.join(reversed_truncated_post_texts)
    )
    # Декодирование содержимого ответа в строку
    page_content = response.content.decode('utf-8')
    # Выполни поиск по обновленному шаблону
    assert re.search(reversed_post_list_pattern, page_content), (
        'Убедитесь, что на странице `{url}` отображается перевернутый список'
        'текстов сообщений из задания'
    )
