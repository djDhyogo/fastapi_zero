from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.models import User
from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client: TestClient):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_retornar_html_deve_retornar_html(client: TestClient):
    response = client.get('/retornar_html')
    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
<html>
    <head>
        <title>Olá Mundo!</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <h1>Olá Mundo!</h1>
    </body>
</html>
    """
    )


def test_create_user_ja_existe_409(client: TestClient, user: User):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_email_ja_existe_409(client: TestClient, user: User):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste1',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_deve_retornar_201(client: TestClient):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste1',
            'email': 'dj@example.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Teste1',
        'email': 'dj@example.com',
    }


def test_read_users(client: TestClient, user: User):
    """
    Testa se o endpoint GET /users/ retorna a lista de usuários.
    para isso ele Cria um usuário usando o fixture create_user_test
    """
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Teste',
                'email': 'teste@test.com',
            }
        ]
    }


def test_read_users_with_users(client: TestClient, user: User):
    """
    Testa se o endpoint GET /users/ retorna a lista de usuários.
    para isso ele Cria um usuário usando o fixture create_user_test
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client: TestClient, user: User):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@test.com',
    }


def test_get_user_retornar_404(client: TestClient):
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user(client: TestClient, user: User):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'string',
        },
    )
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'string',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already registered!'
    }


def test_delete_user(client: TestClient, user: User):
    reponse = client.delete('/users/1')
    assert reponse.status_code == HTTPStatus.OK
    assert reponse.json() == {'message': 'User deleted!'}


def test_delete_user_deve_retornar_404(client: TestClient):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
