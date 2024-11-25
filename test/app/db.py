from fastapi import Depends
from fastapi.params import Depends as DependsType
from bjs_sqlalchemy.models.config import DatabaseConfig, AsyncDatabaseConfig
from sqlalchemy.orm import Session as DBSession

DATABASE_URL = "sqlite:///database.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///database.db"
DEBUG=False


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
        
        # return DatabaseConfig(db_url=DATABASE_URL)

    

class SessionMixin:
    @property
    def session(self):
        return Session()
    
class AsyncSession:
    async def __new__(cls):
        return await AsyncDatabaseConfig(db_url=ASYNC_DATABASE_URL, debug=DEBUG)

class AsyncSessionMixin:
    @property
    def session(self):
        return AsyncSession()

