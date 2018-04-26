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

        


users = []
meals = []
menu = []
orders = []

### To add new user during signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.get_json().get('username', None)
    password = request.get_json().get('password')
    email = request.get_json().get('email', None)
    encrypted_password =generate_password_hash(password, method='sha256')

    user = User(username=username, password=encrypted_password, email=email)
    users.append(user.to_dict())
    print(users)
    return jsonify(user.to_dict())

##### During log in

# Get username and password from request then login user if successfull
@app.route('/signin', methods=['POST'])
def login():
    for user in users:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if user['username'] == username:
            if check_password_hash(user['password'], password):
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
    #Create an instance of Meal
    meal = Meal(food=food, price=price, id=id)
    meals.append(meal.to_dict())
    #user.add_meal(meal)
    print(meal.to_dict())
    return jsonify(meal.to_dict())

#To get meal option by admin
@app.route('/get_meals', methods=['GET'])
def get_meals():
    return jsonify(meals)

#update a meal option by admin
@app.route('/mordify_meal/<int:id>', methods=['PUT'])
def mordify_meal(id):
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')
    new_id = request.get_json().get('id')
    new_meal = Meal(food=new_food, price=new_price, id=new_id)
    prev_food = []
    #Finding the meal to be modified by id
    for i in meals:
        if i['id'] == id:
            prev_food.append(i)
    print(prev_food)
    #Replacing the  previous meal by the new meal
    for i,item in enumerate(meals):
        if item == prev_food[0]:
            meals[i]=new_meal.to_dict()
    return jsonify(meals)

#Remove  A meal option
@app.route('/delete/<int:id>/', methods=['DELETE'])
def delete(id):
    for i in meals:
        if i['id'] == id:
            print(i)
            meals.remove(i)
    return jsonify(meals)

#Set menu for a day
@app.route('/setmenu/', methods=['POST'])
def setmenu():
    food = request.get_json().get('food')
    price = request.get_json().get('price')
    id = request.get_json().get('id')
    new_meal = Meal(food=food, price=price, id=id)
    if new_meal.to_dict() not in meals:
        return jsonify({"message":"Meal not available in system"})
    menu.append(new_meal.to_dict())
    return jsonify(menu)

#Get the menu for the day
@app.route('/getmenu/', methods=['GET'])
def getmenu():
    return jsonify(menu)

#Select meal from menu
@app.route('/selectmeal/<int:id>', methods=['POST'])
def selectmeal(id):
    for i in menu:
        if i['id'] == id:
            orders.append(i)
            return jsonify(orders)
    return jsonify(orders)

#Get all orders
@app.route('/orders/all/')
def allorders():
    return jsonify(orders)

#Modify an order
@app.route('/orders/<int:id>', methods=['PUT'])
def oneorder(id):
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





if __name__ == '__main__':
    app.run(port=7300, debug=True)
