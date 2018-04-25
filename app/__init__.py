from flask import Flask, request, jsonify
app = Flask(__name__)
import json

menu= []

users = [{"username": "Tom", "password":"tomylin", "email":"tomemail"},
        {"username": "Angie", "password":"angelican", "email":"angelmail"}]

orders = [{"food":"beeans and chapati", "id":4, "price":200}]
meals = [{"food":"pilau and beef", "id":3, "price":350}]

#login endpoint
@app.route('/login')
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
@app.route('/register', methods=['POST'])
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
@app.route('/menu/', methods=['GET'])
def getmenu_endpoint():
    data = jsonify(menu)
    return data

#api endpoint for making an order basing on the menu
@app.route('/makeorder', methods=['GET', 'POST'])
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
