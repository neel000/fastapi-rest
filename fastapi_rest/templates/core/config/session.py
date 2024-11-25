from fastapi import Depends
from fastapi.params import Depends as DependsType
from .settings import DATABASE_URL, DEBUG, ASYNC_DATABASE_URL
from bjs_sqlalchemy.models.config import DatabaseConfig, AsyncDatabaseConfig
from sqlalchemy.orm import Session as DBSession


def get_db():
    db = DatabaseConfig(db_url=DATABASE_URL)
    try:
        yield db
    finally:
        db.close()

class Session:
    _session: DBSession = Depends(get_db)
    def __new__(cls):
        if isinstance(cls._session, DependsType):
            return next(get_db())

class SessionMixin:
    _session: DBSession = Depends(get_db)
    @property
    def session(self) -> DBSession:
        if isinstance(self._session, DependsType):
            return next(get_db())

class AsyncSession:
    def __new__(cls):
        return AsyncDatabaseConfig(db_url=ASYNC_DATABASE_URL, debug=DEBUG)

class AsyncSessionMixin:
    @property
    def session(self):
        return AsyncSession()

