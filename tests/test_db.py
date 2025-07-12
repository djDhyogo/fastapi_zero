from dataclasses import asdict

from sqlalchemy import Select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:  # Chamando o mock criado no
        # confistest para inserir uma data fixa
        new_user = User(
            username='alise', email='dj@example.com', password='123456'
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(Select(User).where(User.username == 'alise'))

        assert asdict(user) == {
            'id': 1,
            'username': 'alise',
            'email': 'dj@example.com',
            'password': '123456',
            'created_at': time,
            'updated_at': time,
        }
