import unittest 
import json
import app

BASE_URL = '/api/v1'


class EndPointsTestCase(unittest.TestCase):
    """ Tests for all the api endpoints """
    def setUp(self):
        """ Initialize app and define test variables"""
        app.testing=True
        self.app = app.app.test_client()

        self.user = {"username":"Larry", "password":"larrypage", "email":"larry@paw", "is_admin":True}
        self.user_normal = {"username":"Normar", "password":"larrypage", "email":"mon@paw"}
        
        self.user_login = {'username':'Larry','password':'larrypage'}
        self.user_normal_login = {'username':'Normar', "password":'larrypage', 'token':'oeoie0'}
        self.meal = {"food":"githeri", "price":450, "id":1}
        self.meal1 = {"food":"spagheti", "price":250, "id":2}
        self.meal2 = {"price":400}
        self.meal4 = {"food":"mutton", "price":500, "id":4}
        self.orders = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]
        self.user1 = [{"username":"manu", "password":"manu0", "id":1}]
        self.menu = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]

        response = self.app.post('/signup', data=json.dumps(self.user),content_type='application/json')
        response = self.app.post('/signin', data=json.dumps(self.user_login),content_type='application/json')
        self.token = json.loads(response.data).get('token')


    def test_signup(self):
        """ Test API endpoint can register a new user"""
        response = self.app.post('/signup', data=json.dumps(self.user_normal),content_type='application/json')
        self.token = json.loads(response.data).get('token')
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """"Test API endpoint can login user"""
        res = self.app.post('/signin', data=json.dumps(self.user_login), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue('token' in data)


    
    
    def test_addmeal_endpoint(self):
        """ Test API endpoint can add meal"""
        response = self.app.post('/meals', data=json.dumps(self.meal), content_type='application/json', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 201)
        res = self.app.delete('/meal/1', headers={'x-access-token':self.token})
        self.assertEqual(res.status_code, 200)
        



    def test_deletemeal_endpoint(self):
        """Test API endpoint can delete meal"""
        meal = {"food":"githeri", "price":450, "id":10}
        response = self.app.post('/meals', data=json.dumps(meal), content_type='application/json', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 201)
        res = self.app.delete('/meal/10', headers={'x-access-token':self.token})
        self.assertEqual(res.status_code, 200)

         #Test to see if it exists, should return a 404
        result = self.app.get('/meal/10', headers={'x-access-token':self.token})
        self.assertEqual(result.status_code, 404)
        

    def test_modifymeal_endpoint(self):
        """Test API endpoint can modify meal option """
        response = self.app.post('/meals', data=json.dumps(self.meal1), content_type='application/json', headers={'x-access-token':self.token})
        response = self.app.put('/meal/2', data=json.dumps(self.meal2), content_type='application/json', headers={'x-access-token':self.token})
    
        self.assertEqual(response.status_code, 200)
        req = self.app.get('/meal/2', headers={'x-access-token':self.token})
        data = json.loads(req.get_data()).get('price')
        self.assertEqual(data, 400)
        


    def test_getonemeal_endpoint(self):
        """ Test API endpoint can get one meal given the meal id"""
        response = self.app.post('/meals', data=json.dumps(self.meal4), content_type='application/json', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        result = self.app.get('/meal/{}'.format(data.get('id')), headers={'x-access-token':self.token})
        self.assertEqual(result.status_code, 200)
        
        

    def test_getmeals_endpoint(self):
        """Test API endpoint can get all meals"""
        req = self.app.get('/meals',
                            headers={'x-access-token':self.token})
        self.assertEqual(req.status_code, 200)
    

    def test_getmenu_endpoint(self):
        """Test API endpoint can get menu"""
        req = self.app.get('/menu' , headers={'x-access-token':self.token})
        self.assertEqual(req.status_code, 200)


    def test_modifyorder_endpoint(self):
        """Test API endpoint can modify order option """
        response = self.app.post('/meals', data=json.dumps(self.meal1), content_type='application/json', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/menu', data=json.dumps(self.meal1), content_type='application/json', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/menu/2', headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.app.put('/order/2', data=json.dumps(self.meal2), content_type='application/json', headers={'x-access-token':self.token})
        
        self.assertEqual(response.status_code, 200)
        req = self.app.get('/order/2', headers={'x-access-token':self.token})
        data = json.loads(req.get_data()).get('price')
        self.assertEqual(data, 400)


    def test_alloders_endpoint(self):
        """ Test API endpoint can get all orders """
        req = self.app.get('/orders', headers={'x-access-token':self.token})
        self.assertEqual(req.status_code, 200)

    def test_getoneoder_endpoint(self):
        """Test API endpoint can get one order"""
        req = self.app.get('/order/1', headers={'x-access-token':self.token})
        data = json.loads(req.get_data())
        self.assertEqual(req.status_code, 200)
        self.assertIn('githeri', str(data))




if __name__ == "__main__":
    unittest.main()


