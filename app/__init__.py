from flask import Flask, request, jsonify, abort, make_response
import json
import uuid
import os
import jwt
from functools import wraps
import datetime
from werkzeug.security  import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ER9U9U9N9EUR'

class User():
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    


    def to_dict(self):
        return {"username":self.username, "password":self.password, "email":self.email}
      
      
class Order():
    def __init__(self, food, price, id):
        self.food = food
        self.price = price
        self.id = id

    def to_dict(self):
        return {"food":self.food, "price":self.price, "id":self.id} 
      
class Meal():
    def __init__(self, food, price, id):
        self.food = food
        self.price = price
        self.id = id

    
    def to_dict(self):
        return {"food":self.food, "price":self.price, "id":self.id}

        

order = []
users = []
meals = []
menu = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]
orders = [{"food":"githeri", "price":450, "id":1},{"food":"spagheti", "price":250, "id":2}]

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'message':'Token is missing!'}), 401

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = request.get_json.get('id')
		except:
			return jsonify({'message': 'Token is invalid!'}), 401

		return f(current_user, *args, **kwargs)

	return decorated 

### To add new user during signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.get_json().get('username', None)
    password = request.get_json().get('password')
    email = request.get_json().get('email', None)
    encrypted_password =generate_password_hash(password, method='sha256')
    token = jwt.encode({'token': email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})

    user = User(username=username, password=encrypted_password, email=email)

    users.append(user.to_dict())
    return jsonify({'token': token.decode('UTF-8')})

##### During log in

# Get username and password from request then login user if successfull
@app.route('/signin', methods=['POST'])
@token_required
def login():
    for user in users:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                token = jwt.encode({'token': user['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})
                
            else:
                return "Invalid password"
      
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

      
####### TO add a meal for a given user
@app.route('/add_meal', methods=['POST'])
def add_meal():
    food = request.get_json().get('food')
    price = request.get_json().get('price')
    id = request.get_json().get('id')
    #Create an instance of Meal
    meal = Meal(food=food, price=price, id=id)
    meals.append(meal)
    #user.add_meal(meal)
    return jsonify(meal.to_dict())

#To get meal option by admin
@app.route('/meals/', methods=['GET'])
@token_required
def getmeals_endpoint():
    meal_res = {
        'meals':[meal.to_dict()  for meal in meals]
    }
    return jsonify(meal_res)

#update a meal option by admin
@app.route('/mordify_meal/<int:id>', methods=['PUT'])

def mordify_meal(id):
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')

    for meal in meals:
        if meal.id == id:
            meal.food = new_food
            meal.price = new_price
            return jsonify(meal.to_dict()), 200

    return abort(404)

#Remove  A meal option
@app.route('/delete/<int:id>', methods=['GET','DELETE'])
def delete(id):
    for i in meals:
        if i.id == id:
            meals.remove(i)
            return jsonify({"Message":"Meal deleted"}) , 200
    return jsonify({"message":"Item not found"}), 404

#Set menu for a day
@app.route('/setmenu', methods=['POST'])
def setmenu():
    food = request.get_json().get('food')
    price = request.get_json().get('price')
    id = request.get_json().get('id')
    new_meal = Meal(food=food, price=price, id=id)
    meal_res = {
        'meals':[meal.to_dict()  for meal in meals]
    }
    if new_meal not in meal_res:
        return jsonify({"message":"Meal not available in system"})
    menu.append(new_meal.to_dict())
    return jsonify(menu)

#Get the menu for the day
@app.route('/getmenu/', methods=['GET'])
def getmenu_endpoint():
    return jsonify(menu)

#Select meal from menu
@app.route('/meal/<int:id>', methods=['GET'])
def meal(id):
    for meal in meals:
        if meal.id == id:
            return jsonify(meal.to_dict()), 200
    return abort(404)


#Get all orders
@app.route('/orders')
def allorders_endpoint():
    return jsonify(orders)

#Modify an order
@app.route('/orders/<int:id>', methods=['PUT'])
def modifyorder_endpoint(id):
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')
    new_id = request.get_json().get('id')
    new_order = Order(food=new_food, price=new_price, id=new_id)
    prev_order = []
    #Findng the previous order by id provided in the route
    for i in orders:
        if i['id'] == id:
            prev_order.append(i)
    print(prev_order)
    #Replacing the privious order with the new order
    for i,item in enumerate(orders):
        if item == prev_order[0]:
            orders[i]=new_order.to_dict()
    return jsonify(orders)


#Select order from orders
@app.route('/selectorder/<int:id>', methods=['GET'])
def getoneorder_endpoint(id):
    for i in orders:
        if i['id'] == id:
            order.append(i)
            return jsonify(order)
    return jsonify(order)

#update a meal option by admin
@app.route('/mordify/<int:id>', methods=['PUT'])
def mordify_order(id):
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')

    for meal in orders:
        if meal.id == id:
            meal.food = new_food
            meal.price = new_price
            return jsonify(meal.to_dict()), 200

    return abort(404)

if __name__ == "__main__":
    app.run(port=7300, debug=True)