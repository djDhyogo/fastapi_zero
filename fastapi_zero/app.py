from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


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
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(db_user)  # adiciona Sesion
    session.commit()  # envia para o banco
    session.refresh(db_user)  # atualiza a sesion

    return db_user


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User).limit(limit).offset(offset),
    )

    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        # O usuario com esse id  nao existe no banco
        raise HTTPException(
            detail='User not found!',
            status_code=HTTPStatus.NOT_FOUND,
        )

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        # O usuario com esse id  nao existe no banco
        raise HTTPException(
            detail='User not found!',
            status_code=HTTPStatus.NOT_FOUND,
        )
    session.delete(db_user)
    session.commit()

    return Message(message='User deleted!')


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user__exercicio(
    user_id: int, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    return db_user
