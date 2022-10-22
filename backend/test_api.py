import unittest


import unittest
# from backend.recipe import HelloResource
from config import TestConfig
from main import create_app
from exts import db
class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_hello_world(self):
        hello_resource = self.client.get('/recipe/hello')
        json = hello_resource.json

        self.assertEqual(json,{"Message": "Hello World"})

    def test_signup(self):
        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        self.assertEqual(signup_response.status_code,201)
        self.assertEqual(signup_response.json.get('Message'),"New user created successfully")


    def test_login(self):
        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        
        login_response = self.client.post('/auth/login', json={"username": "user", "password": "password"})
        self.assertEqual(login_response.status_code, 200)

    def test_get_all_recipies(self):
        recipes_response = self.client.get('/recipe/recipes')
        self.assertEqual(recipes_response.status_code, 200)

    def test_get_one_recipe(self):

        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        
        login_response = self.client.post('/auth/login', json={"username": "user", "password": "password"})
        access_token = login_response.json['access_token']
        id = 1
        recipes_response = self.client.get(f'/recipe/recipe/{id}',
        headers={'Authorization': 'Bearer ' + access_token})
        
        self.assertEqual(recipes_response.status_code,404)


    def test_create_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        
        login_response = self.client.post('/auth/login', json={"username": "user", "password": "password"})
        access_token = login_response.json['access_token']
        recipes_response = self.client.post('/recipe/recipes', 
        json={"title": "recipe", "description": "recipe description"},
        headers={"Authorization": "Bearer " + access_token})
        self.assertEqual(recipes_response.status_code, 200)
    def test_update_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        
        login_response = self.client.post('/auth/login', json={"username": "user", "password": "password"})
        access_token = login_response.json['access_token']
        recipes_response = self.client.post('/recipe/recipes', 
        json={"title": "recipe", "description": "recipe description"},
        headers={"Authorization": "Bearer " + access_token})
        self.assertEqual(recipes_response.status_code, 200)
        id =1
        recipes_response_update = self.client.put(f'/recipe/recipe/{id}', 
        json={"title": "recipe11", "description": "recipe description11"},
        headers={"Authorization": "Bearer " + access_token})
        self.assertEqual(recipes_response_update.status_code, 200)
        

    def test_delete_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json={"username": "user", "password": "password","email": "user@example.com"})
        
        login_response = self.client.post('/auth/login', json={"username": "user", "password": "password"})
        access_token = login_response.json['access_token']
        
        recipes_response = self.client.post('/recipe/recipes', 
        json={"title": "recipe", "description": "recipe description"},
        headers={"Authorization": "Bearer " + access_token})
        print(recipes_response.json) 
        self.assertEqual(recipes_response.status_code, 200)
        id =1
        recipes_response_delete = self.client.delete(f'/recipe/recipe/{id}',
        headers={"Authorization": "Bearer " + access_token})
        print(recipes_response_delete.json) 
        self.assertEqual(recipes_response_delete.status_code, 200)

if __name__ == '__main__':
    unittest.main()