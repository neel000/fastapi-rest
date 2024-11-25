from app import main
from app.models import TestModel
from fastapi_rest.testclient import TestClient as FastApiTestClient, session

class TestClient(FastApiTestClient):
    @classmethod
    def app_name(cls):
        return main.app
    
# def fixtures(models):
#     TestClient.setUpClass
#     session = TestClient.session
#     # _, data = models().bulk_create(session=session, data=[])
#     # print(data)

#     c = session.query(models).count()

#     print(c)
#     def func_wrapper(fun):
#         def wrapper(*args, **kwargs):
#             return fun(*args, **kwargs)
#         return wrapper
   
#     return func_wrapper

class TestIntregration(TestClient):
    def test_valid_path(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_invalid_path(self):
        resp = self.client.get("/hjbrl")
        self.assertEqual(resp.status_code, 404)
    
    def test_async_valid_path(self):
        resp = self.client.get("/async-view")
        self.assertEqual(resp.status_code, 200)
    
    @session.mock_session
    def test_session(self, _):
        resp = self.client.get("/session-test")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['url'], self.database_url)
    
    @session.mock_async_session
    def test_async_session(self, _):
        resp = self.client.get("/async-session-test")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['url'], self.asyn_database_url)

class TestModelCRUD(TestClient):
    models = TestModel

    def test_models_query(self):
        session = self.session
        count = session.query(TestModel).count()
        self.assertEqual(count, 0)
    
    def test_models_create_delete(self):
        status, data = TestModel(name="test").save(session=self.session)
        self.assertEqual(status, True)
        status, _, = data.delete(session=self.session)
        self.assertEqual(status, True)
    
    def test_bulk_create_delete(self):
        session = self.session
        data = [
            {"name":"Test-1"},
            {"name":"Test-2"},
        ]
        status, data = self.models().bulk_create(session=session, data=data)
        self.assertEqual(status, True)

        count = session.query(self.models).count()
        self.assertEqual(count, 2)

        status, _ = self.models().bulk_delete(session=session, data=[1,2])
        self.assertEqual(status, True)

        count = session.query(self.models).count()
        self.assertEqual(count, 0)
        session.close()

@session.mock_session
class TestModelViewSet(TestClient):
    models = TestModel

    base_url = "/viewset"
    def test_list(self, _):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 200)
        
        self.assertEqual(resp.json(), [])
    
    def test_list_with_pagination(self, _):
        resp = self.client.get(f"{self.base_url}?limit=5")
        self.assertEqual(resp.status_code, 200)
        output = {
            'pagination': {
                'count': 0, 
                'total_pages': 0, 
                'next_page': None, 
                'previous_page': 0
            },
            'results': []
        }
        self.assertDictEqual(resp.json(), output)

    def test_crud(self, _):
        resp = self.client.post(self.base_url, json={"name":"Test", "age":30})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        output = {'id': data['id'], 'name': 'Test', 'age': 30}

        resp = self.client.get(f"{self.base_url}/{data['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Update
        resp = self.client.put(
            f"{self.base_url}/{data['id']}", 
            json={"name":"UpdateTest", "age":10}
        )
        output = {'id': data['id'], 'name': 'UpdateTest', 'age': 10}
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Partial Update
        resp = self.client.patch(
            f"{self.base_url}/{data['id']}", 
            json={"age":31}
        )
        output['age'] = 31
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Delete
        resp = self.client.delete(f"{self.base_url}/{data['id']}")
        self.assertEqual(resp.status_code , 204)

    def test_filter_data(self, _):
        data = [
            {"name":"Test-1", "age":30},
            {"name":"Test-2", "age":18},
            {"name":"Test-3", "age":25},
        ]
        _, result = self.models().bulk_create(session=self.session, data=data)

        resp = self.client.get(f"{self.base_url}?name=1")
        self.assertEqual(len(resp.json()), 0)

        resp = self.client.get(f"{self.base_url}?name=Test-1")
        self.assertEqual(len(resp.json()), 1)

        resp = self.client.get(f"{self.base_url}?name__icontains=tddffft")
        self.assertEqual(len(resp.json()), 0)

        resp = self.client.get(f"{self.base_url}?name__icontains=test-1")
        self.assertEqual(len(resp.json()), 1)
        resp = self.client.get(f"{self.base_url}?name__icontains=test-")
        self.assertEqual(len(resp.json()), 3)

        id_list = [i+1 for i in range(result)]   
        self.models().bulk_delete(session=self.session, data=id_list)

@session.mock_async_session
class TestAsyncModelViewSet(TestClient):
    base_url = "/async-viewset"
    def test_list(self, _):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])
    
    def test_list_with_pagination(self,_):
        resp = self.client.get(f"{self.base_url}?limit=5")
        self.assertEqual(resp.status_code, 200)
        output = {
            'pagination': {
                'count': 0, 
                'total_pages': 0, 
                'next_page': None, 
                'previous_page': 0
            },
            'results': []
        }
        self.assertDictEqual(resp.json(), output)

    def test_crud(self, _):
        resp = self.client.post(self.base_url, json={"name":"Test", "age":30})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        output = {'id': data['id'], 'name': 'Test', 'age': 30}

        resp = self.client.get(f"{self.base_url}/{data['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Update
        resp = self.client.put(
            f"{self.base_url}/{data['id']}", 
            json={"name":"UpdateTest", "age":10}
        )
        output = {'id': data['id'], 'name': 'UpdateTest', 'age': 10}
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Partial Update
        resp = self.client.patch(
            f"{self.base_url}/{data['id']}", 
            json={"age":31}
        )
        output['age'] = 31
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), output)

        #Delete
        resp = self.client.delete(f"{self.base_url}/{data['id']}")
        self.assertEqual(resp.status_code , 204)

