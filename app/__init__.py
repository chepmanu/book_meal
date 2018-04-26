'''
from flask import Flask, request, jsonify
app2 = Flask(__name__)
import json

menu= []

users = [{"username": "Tom", "password":"tomylin", "email":"tomemail"},
        {"username": "Angie", "password":"angelican", "email":"angelmail"}]

orders = [{"food":"beeans and chapati", "id":4, "price":200}]
meals = [{"food":"pilau and beef", "id":3, "price":350}]

#login endpoint
@app2.route('/login')
def login():
    user = request.get_json()
    username = user['username']
    password = user['passwowrd']
    if not username:
        return jsonify({"message":"username not filled"})
    if not password:
        return jsonify({"message":"password not given"})
        
    pass
    #still woiking on it

#registration endpoin
@app2.route('/register', methods=['POST'])
def register():
    new_user = request.get_json()
    username = new_user['username']
    password = new_user['password']
    email = new_user['email']
    if not username:
        return jsonify({"message":"username is required"})
    if  not password:
        return jsonify({"message":"password is required"})
    if not email:
        return jsonify({"message":"email is required"})
    if new_user in users:
        return jsonify({"message":"cannot register user"})
    users.append(new_user)
    return jsonify({"message":"registered successfully"})
    
    
#api endpoint for viewing the set menu.
@app2.route('/menu/', methods=['GET'])
def getmenu_endpoint():
    data = jsonify(menu)
    return data

#api endpoint for making an order basing on the menu
@app2.route('/makeorder', methods=['GET', 'POST'])
def selectmealfrommenu_endpoint():
    order = request.get_json()
    if menu is None:
        return jsonify({"message":"no item in menu"})
    if order in orders:
        return jsonify({"message":"order already set"})
    if order not in menu:
        return jsonify({"message":"order not in menu"})
    orders.append(order)
    return ({"message":"order taken successfully"})
#order modification endpoint
@app.route('/modifyorder/<int:id>/', methods=['PUT'])
def modifyorder_endpoint(id):
    order = request.get_json()
    prev_food = []
    for food in menu:
        if food['id'] == id:
            prev_food.append(food)
    #if order not in orders:
    #    return jsonify({"message":"order not found"})
    
    for i,item in enumerate(menu):
        if item == prev_food[0]:
            menu[i]=order

    print(menu)
    return jsonify({"message":"item updated successfully"})

#adding meal endpoint
@app.route('/caterer/add/', methods= ['POST'])
def addmeal_endpoint():
    meal = request.get_json()
    menu.append(meal)
    return jsonify({"message":"meal added successfully"}), 201

#deleting meal endpoint
@app.route('/caterer/delete/<id>', methods=['DELETE'])
def deletemeal_endpoint(id):
    for item in menu:
        if item['id'] == id:
            menu.remove(item)
    print(menu)
    return json.dumps(menu)

#getting one meal endpoint
@app.route('/meal/<int:id>' , methods=['GET'])
def getonemeal_endpoint(id):
    for item in menu:
        if item['id'] == id:
            print(item)
    return json.dumps(item)

#getting all orders endpoint    
@app.route('/caterer/orders/all', methods=['GET'])
def getallorders_endpoint():
    return json.dumps(orders)

#getting all meals endpoint
@app.route('/caterer/meals/all', methods = ['GET'])
def getallmeals():
    return jsonify(meals)
#getting one order endpoint
@app.route('/caterer/order/one/<id>', methods=['GET'])
def getoneoder_endpoint(id):
    for item in orders:
        if item['id'] == id:
            print(item)
    return json.dumps(item)

    
    
if __name__ == "__main__":
    app.run(port=6500)
'''
'''
from flask import Flask, request, jsonify
import json
import uuid
import os
#import jwt
from functools import wraps
import datetime
from werkzeug.security  import generate_password_hash, check_password_hash
app = Flask(__name__)


class User():
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        orders = []
      
    #def add_meal(self, meal):
     #   self.meals.append(meal)

    def getalldetails(self):
        return (self.username, self.password, self.email)
      
      
class Order():
    def __init__(self, food, price):
        self.food = food
        self.price = price
      
class Meal():
    def __init__(self, food, price, id):
        self.food = food
        self.price = price
        self.id = id

    
    def __iter__(self):
        return self.__dict__.iteritems()
        


users = []
meals = []
### To add new user during signup
@app.route('/signup', methods=['POST'])
def register_endpoint():
    username = request.get_json().get('username', None)
    password = request.get_json().get('password')
    email = request.get_json().get('email', None)

    user = User(username=username, password=password, email=email)
    users.append(user)
    print(users)
    return jsonify({"message":"Signed up"})

##### During log in

# Get username and password from request then
@app.route('/login', methods=['POST'])
def login():
    for user in users:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if user.username == username:
            if user.password == password:
                return "login success"
            else:
                return "Invalid password"
      
    return 'Invalid username'
      
####### TO add a meal for a given user
@app.route('/add_meal', methods=['POST'])
def add_meal():
    food = request.get_json().get('food')
    price = request.get_json().get('price')
    id = request.get_json().get('id')
    #get user from list then 

    meal = Meal(food=food, price=price, id=id)
    meals.append(meal)
    #user.add_meal(meal)
    print(meal.food)
    print(dict(meal))
    return jsonify({"message":"meal added"})

#To get meal option by admin
@app.route('/get_meals', methods=['GET'])
def get_meals():
    for i in meals:
        print(i.food)
    return jsonify({"message":"This are the items"})

#update a meal option by admin
@app.route('/mordify_meal/<id>', methods=['PUT'])
def mordify_meal(id):
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')
    new_id = request.get_json().get('id')
    new_meal = Meal(food=new_food, price=new_price, id=new_id)
    prev_food = []
    #for i in meals:
   #     if i.id == id:
    #        meals.remove(i)
    for i in meals:
        if i.id == id:
            prev_food.append(i.food)
    print(prev_food)
    print(new_meal.food)
    #if order not in orders:
    #    return jsonify({"message":"order not found"})
    
    for i,item in enumerate(meals):
        if item == prev_food[0]:
            meals[i]=new_meal
    for i in meals:
        print(i.food)
    return jsonify({"message":"Done"})

#Remove  A meal option
@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    for i in meals:
        if i.id == id:
            meals.remove(i)
    for i in meals:
        print(i.food)
    return jsonify({"message":"Item removed"})


if __name__ == '__main__':
    app.run(port=7300, debug=True)
'''