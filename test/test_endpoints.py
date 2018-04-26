import unittest 
import json
import app

BASE_URL = 'http://127.0.0.1:6500/api/v1/user/'

class EndPointsTestCase(unittest.TestCase):
    """ Tests for all the api endpoints """
    def setUp(self):
        """ Initialize app and define test variables"""
        self.app = app.app.test_client()
        self.user = {"id":2, "name":"username", "password":"userpassword"}
        self.meal2 = {"id":1, "food": "rice and beef", "price":450}
        self.meal = {"id":2, "food":"spagheti", "price":250}
        self.meals = {
            'meal1':{
                "id":3,
                "food":"beef",
                "price":300
            },
            'meal2':{
                "id":4,
                "food":"pasta",
                "price":350
            }
        }
        
        self.orders = {
            'order1':{
                "id":3,
                "food":"eggs",
                "price":300
            },
            'order2':{
                "id":4,
                "food":"fries",
                "price":350
            }
        }


    def test_register_endpoint(self):
        """ Test API endpoint can register a new user"""
        response = self.app.post(BASE_URL+'/register', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """"Test API endpoint can login user"""
        res = self.app.post(BASE_URL+'/login', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)
    
    def test_addmeal_endpoint(self):
        """ Test API endpoint can add meal"""
        response = self.app.post(BASE_URL+'/caterer/add/{}'.format('id'), data=json.dumps(self.meal2), content_type='application/json')
        self.assertEqual(response.status_code, 201)


    def test_deletemeal_endpoint(self):
        """Test API endpoint can delete meal"""
        res1 = self.app.post(BASE_URL+'/caterer/add/{}'.format('id'), data=json.dumps(self.meal2), content_type='applicatin/json')
        self.assertEqual(res1.status_code, 201)
        res = self.app.delete(BASE_URL+'/caterer/delete/1')
        self.assertEqual(res.status_code, 200)
        res = self.app.delete(BASE_URL+ '/1')
        self.assertEqual(res.status_code, 404)

    def test_modifymeal_endpoint(self):
        """Test API endpoint can modify meal option """
        self.meal1 = {"price":500}
        response1 = self.app.put(BASE_URL+'/caterer/modify/3/', data=json.dumps(self.meal1), content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        data = self.app.get(BASE_URL+'/meal/3/')
        self.assertEqual(data["price"], 500)


    def test_getonemeal_endpoint(self):
        res = self.app.get(BASE_URL+'/meal/3/')
        self.assertEquals(res.status_code, 200)
        data = json.loads(res.get_data())
        self.assertIn('beef', data["food"])


    def test_getallmeals_endpoint(self):
        req = self.app.get(BASE_URL+ '/catererer/meals/all/')
        self.assertEqual(req.status_code, 200)
        self.assertIn('rice and beef', str(req.data))

    def test_getmenu_endpoint(self):
        req = self.app.get(BASE_URL+'/menu')
        self.assertEqual(req.status_code, 200)
        data = json.loads(req.get_data())
        self.assertEqual(req.status_code, 200)
        self.assertIn('pasta', str(data["food"]))

    def test_selectmealfrommenu_endpoint(self):
        res = self.app.get(BASE_URL+'/menu/')
        self.assertEqual(res.status_code, 200)
        res = self.app.post(BASE_URL+'/menu/1')
        data = json.loads(res.get_data())
        self.assertEqual(res.status_code, 200)
        self.assertIn('rice and beef', data["food"])

    def test_modifyorder_endpoints(self):
        self.meal6 = {"food": "plantain"}
        res = self.app.get(BASE_URL+'/order/3')
        self.assertEqual(res.status_code, 200)
        res = self.app.put(BASE_URL+'/order/3', data=json.dumps(self.meal6), content='application/json')
        self.assertEqual(res.status_code, 400)

    def test_getalloders_endpoint(self):
        req = self.app.get(BASE_URL+'/caterer/orders/all')
        self.assertEqual(req.status_code, 200)
        data = json.loads(req.get_data())
        self.assertIn('fries', data["order2"])




if __name__ == "__main__":
    unittest.main()


