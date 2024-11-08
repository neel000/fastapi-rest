from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from fastapi.params import Depends as DependsType
from sqlalchemy.ext.asyncio import AsyncSession
from .settings import DATABASE_URL, DEBUG

class DatabaseConfig:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            engine = create_engine(DATABASE_URL, echo=DEBUG)
            Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            cls._instance = Session()
        return cls._instance

def get_db():
    db = DatabaseConfig()
    try:
        yield db
    finally:
        db.close()

class DBSession:
    __session: AsyncSession = Depends(get_db)
    def __new__(cls):
        if isinstance(cls.__session, DependsType):
            return next(get_db())

class DBSessionMixin:
    __session: AsyncSession = Depends(get_db)
    @property
    def session(self) -> AsyncSession:
        if isinstance(self.__session, DependsType):
            return next(get_db())

