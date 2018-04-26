import unittest 
import json
import app

BASE_URL = 'http://127.0.0.1:6500/api/v1/'


class EndPointsTestCase(unittest.TestCase):
    """ Tests for all the api endpoints """
    def setUp(self):
        """ Initialize app and define test variables"""
        app.testing=True
        self.app = app.app.test_client()

        self.user = {"username":"Larry", "password":"larrypage", "email":"larry@paw"}
        self.meal = {"food":"githeri", "price":450, "id":1}
        self.meal1 = {"food":"spagheti", "price":250, "id":2}
        self.meal2 = {"food":"mutton", "price":500, "id":3}
        self.orders = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]
        self.user1 = [{"username":"manu", "password":"manu0", "id":1}]
        menu = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]




    def test_signup(self):
        """ Test API endpoint can register a new user"""
        response = self.app.post('/signup', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # def test_login_endpoint(self):
    #     """"Test API endpoint can login user"""
    #     res = self.app.post('/signin', data=json.dumps(self.user), content_type='application/json')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(self.user['password'], 'larrypage')
    #     self.assertAlmostEqual(self.user['username'], 'Larry')


    
    
    def test_addmeal_endpoint(self):
        """ Test API endpoint can add meal"""
        response = self.app.post('/add_meal', data=json.dumps(self.meal), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        res = self.app.delete('/delete/1')
        self.assertEqual(res.status_code, 200)


    def test_deletemeal_endpoint(self):
        """Test API endpoint can delete meal"""
        meal = {"food":"githeri", "price":450, "id":10}
        response = self.app.post('/add_meal', data=json.dumps(meal), content_type='application/json')
        res = self.app.delete('/delete/10')
        self.assertEqual(res.status_code, 200)

         #Test to see if it exists, should return a 404
        result = self.app.get('/meal/10')
        self.assertEqual(result.status_code, 404)
        

    def test_modifymeal_endpoint(self):
        """Test API endpoint can modify meal option """
        response = self.app.post('/add_meal', data=json.dumps(self.meal), content_type='application/json')
        response = self.app.put('/mordify_meal/1', data=json.dumps(self.meal2), content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        req = self.app.get('/meal/1')
        self.assertEqual(req.status_code, 200)
        


    def test_getonemeal_endpoint(self):
        """ Test API endpoint can get one meal given the meal id"""
        rv = self.app.post('/add_meal', data=json.dumps(self.meal), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        result_in_json = json.loads(rv.get_data())
        result = self.app.get('/meal/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        
        

    def test_getmeals_endpoint(self):
        """Test API endpoint can get all meals"""
        req = self.app.get('/meals/')
        self.assertEqual(req.status_code, 200)
    

    def test_getmenu_endpoint(self):
        """Test API endpoint can get menu"""
        req = self.app.get('/getmenu/')
        self.assertEqual(req.status_code, 200)
        data = json.loads(req.get_data())
        print(data)
        #self.assertEqual(req.status_code, 200)
        self.assertIn('githeri', str(data))


    def test_modifyorder_endpoint(self):
        """Test API endpoint can modify order """
        response = self.app.post('/add_meal', data=json.dumps(self.meal), content_type='application/json')
        response = self.app.put('/orders/1', data=json.dumps(self.meal2), content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        req = self.app.get('/meal/1')
        self.assertEqual(req.status_code, 200)

    def test_alloders_endpoint(self):
        """ Test API endpoint can get all orders """
        req = self.app.get('/orders')
        self.assertEqual(req.status_code, 200)

    def test_getoneoder_endpoint(self):
        """Test API endpoint can get one order"""
        req = self.app.get('/selectorder/1')
        data = json.loads(req.get_data())
        self.assertEqual(req.status_code, 200)
        self.assertIn('githeri', str(data))




if __name__ == "__main__":
    unittest.main()


