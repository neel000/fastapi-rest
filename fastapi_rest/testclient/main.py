from unittest.mock import patch
from fastapi.testclient import TestClient as AppTestClient
from bjs_sqlalchemy.testclient import TestClient as DBTestClient
from bjs_sqlalchemy.models.config import DatabaseConfig, AsyncDatabaseConfig
from abc import ABC, abstractmethod

class MockSession:
    _client = None

    def __new__(cls):
        if not cls._client:
            DBTestClient.setUpClass()
            cls._client = super().__new__(cls)
            DBTestClient.tearDownClass()
        return cls._client

    @property
    def mock_session(self):
        session =  DBTestClient.session
        return patch.object(DatabaseConfig, '__new__', return_value=session)

    @property
    def mock_async_session(self):
        session = DBTestClient.async_session
        return patch.object(AsyncDatabaseConfig, '__new__', return_value=session)

session = MockSession()

class TestClient(DBTestClient, ABC):
    @classmethod
    @abstractmethod
    def app_name(cls):
        return None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = AppTestClient(cls.app_name())

