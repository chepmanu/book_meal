from flask import request, jsonify, abort, make_response
import json
import jwt

import datetime
from werkzeug.security  import generate_password_hash, check_password_hash
from . import app

from .auth import generate_token, token_required

from .data import users  , User , Meal , meals , menu, order, Order, orders, verify_email

### To add new user during signup
@app.route('/api/v1/auth/signup', methods=['POST'])
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

    #return jsonify({'token': generate_token(user.email)})
    return jsonify({"message":"successful sign up"})
##### During log in

# Get username and password from request then login user if successfull
@app.route('/api/v1/auth/signin', methods=['POST'])
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
@app.route('/api/v1/meals', methods=['POST'])
@token_required
def add_meal(current_user):
    food = request.get_json().get('food')
    price = request.get_json().get('price')
    id = request.get_json().get('id')
    #Create an instance of Meal
    meal = Meal(food=food, price=price)
    meals.append(meal)
    #user.add_meal(meal)
    return jsonify(meal.to_dict()), 201

#To get meal option by admin
@app.route('/api/v1/meals', methods=['GET'])
@token_required
def getmeals_endpoint(current_user):
    if not current_user.is_admin:
        return jsonify({'message':'you must an admin','status':401}), 401
    meal_res = {
        'meals':[meal.to_dict()  for meal in meals]
    }
    return jsonify(meal_res)

#Select meal from menu
@app.route('/api/v1/meal/<int:id>', methods=['GET'])
@token_required
def get_meal(current_user, id):
    for meal in meals:
        if meal.id == id:
            return jsonify(meal.to_dict()), 200
    return abort(404)


#update a meal option by admin
@app.route('/api/v1/meal/<int:id>', methods=['PUT'])
@token_required
def mordify_meal(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')

    for meal in meals:
        if meal.id == id:
            meal.food = new_food
            meal.price = new_price
            return jsonify(meal.to_dict()), 200

    return abort(404)

#Remove  A meal option
@app.route('/api/v1/meal/<int:id>', methods=['DELETE'])
@token_required
def delete(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    for i in meals:
        if i.id == id:
            meals.remove(i)
            return jsonify({"Message":"Meal deleted"}) , 200
    return jsonify({"message":"Item not found"}), 404

#Set menu for a day
@app.route('/api/v1/menu', methods=['POST'])
@token_required
def setmenu(current_user):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    id = request.get_json().get('id')

    meal = list(filter(lambda meal : meal.id == id, meals))

    if not meal:
        return jsonify({"message":"Meal not available in system"})

    menu.append(meal[0])
     
    return jsonify({"message":"success"})

#Get the menu for the day
@app.route('/api/v1/menu', methods=['GET'])
@token_required
def getmenu_endpoint(current_user):
    menu_res = {"menu":[meal.to_dict() for meal in menu]}
    print(menu_res)
    return jsonify(menu_res)


#Select meal from menu
@app.route('/api/v1/orders', methods=['POST'])
@token_required
def meal(current_user):
    id = request.get_json().get('id')
  
    meal = list(filter(lambda meal: meal.id == id  , menu))[0]

    if not meal:
        return abort(404)
    order = Order(meal , current_user )
    orders.append(order)

    return jsonify(order.to_dict()), 201


#Get all orders
@app.route('/api/v1/orders')
@token_required
def allorders_endpoint(current_user):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    print(orders)
    return jsonify({"orders":[order.to_dict() for order in orders]})

#Modify an order
@app.route('/api/v1/order/<int:id>', methods=['PUT'])
@token_required
def modifyorder_endpoint(current_user, id):
    meal_id = request.get_json().get('meal_id')

    order = list(filter(lambda order: order.id == id  , orders))[0]
    if not order:
        return abort(404)

    # Check order is not fullled

    meal = list(filter(lambda meal: meal.id == meal_id  , menu))[0]
    
    if not meal:
        return abort(404)

    order.meal =meal

    return jsonify(order.to_dict())

#Select order from orders
@app.route('/api/v1/order/<int:id>', methods=['GET'])
@token_required
def getoneorder_endpoint(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    for i in orders:
        if i.id == id:
            order.append(i)
            return jsonify(i.to_dict())
    return abort(404)

@app.route('/api/v1/order/<int:id>', methods=['PUT'])
@token_required
def mordify_order(current_user, id):
    if not current_user.is_admin:
        return jsonify({"message":"you must be an admin to perfom this operation", 'status':401}), 401
    new_food = request.get_json().get('food')
    new_price = request.get_json().get('price')

    for meal in orders:
        if meal.id == id:
            meal.food = new_food
            meal.price = new_price
            return jsonify(meal.to_dict()), 200

    return abort(404)