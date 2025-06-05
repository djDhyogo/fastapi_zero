from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

databese = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def root():
    return {'message': 'Olá Mundo!'}


@app.get(
    '/retornar_html', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
async def retornar_html():
    return """
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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(databese) + 1)
    databese.append(user_with_id)
    return user_with_id


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users():
    return {'users': databese}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(databese):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )
    databese[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(databese):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )
    return databese.pop(user_id - 1)


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(databese):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )
    return databese[user_id - 1]
