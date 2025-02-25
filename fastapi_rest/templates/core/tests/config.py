from fastapi_rest.testclient import TestClient as FastApiTestClient
import main

class TestClient(FastApiTestClient):
    @classmethod
    def app_name(cls):
        return main.app