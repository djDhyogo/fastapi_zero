from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_retornar_html_deve_retornar_html(client):
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


def test_create_user_deve_retornar_201(client):
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


def test_read_users(client, user):
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


def test_read_users_with_users(client, user):
    """
    Testa se o endpoint GET /users/ retorna a lista de usuários.
    para isso ele Cria um usuário usando o fixture create_user_test
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@test.com',
    }


def test_get_user_retornar_404(client):
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user(client, user):
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
        'username': 'tes',
        'email': 'bob@example.com',
    }


def test_update_user_deve_retornar_404(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'BOB',
            'email': 'bob@example.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user(client, user):
    reponse = client.delete('/users/1')
    assert reponse.status_code == HTTPStatus.OK
    assert reponse.json() == {'message': 'User deleted!'}


def test_delete_user_deve_retornar_404(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
