from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore


def get_session():
    """
    Fornece uma Session para uso e garante seu fechamento ao final.
    executa o gerador até o yield e, ao finalizar a request, continua o
    gerador para permitir o teardown (fechamento da sessão).
    """
    with Session(engine) as session:
        yield session
