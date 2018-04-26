from flask import request, jsonify, abort, make_response

import json
import uuid
import os
import jwt

import datetime
from werkzeug.security  import generate_password_hash, check_password_hash
from . import app

from .auth import generate_token, token_required

from .data import users  , User , Meal , meals , menu, order, Order, orders, verify_email

### To add new user during signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.get_json().get('username', None)
    password = request.get_json().get('password')
    email = request.get_json().get('email', None)
    is_admin = request.get_json().get('is_admin', None)
    encrypted_password =generate_password_hash(password, method='sha256')

    if not is_admin:
        is_admin = False
    if not verify_email(email):
        return jsonify({"messsage":"email is taken", "status":409}), 409
    user = User(username=username, password=encrypted_password, email=email,is_admin=is_admin)
    users.append(user)

    return jsonify({'token': generate_token(user.email)})

##### During log in

# Get username and password from request then login user if successfull
@app.route('/signin', methods=['POST'])
def login():
    for user in users:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if user.username == username:
            if check_password_hash(user.password, password):
                token = generate_token(user.email)
                return jsonify({'token': token})
                
            else:
                return jsonify({"message":"Invalid password"}), 401
      
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
@app.route('/meals', methods=['GET'])
@token_required
def getmeals_endpoint(current_user):
    if not current_user.is_admin:
        return jsonify({'message':'you must an admin','status':401}), 401
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
    return jsonify({"orders":[order.to_dict() for order in orders]})

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
        if i.id == id:
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
        if i.id == id:
            order.append(i)
            return jsonify(i.to_dict())
    return abort(404)

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