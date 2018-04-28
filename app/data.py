
class User():
    def __init__(self, username, password, email, is_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin


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
menu = []
default_order = Order(food='githeri',price=233,id=1)
orders = [default_order]


def verify_email(email):
    for user in users:
        if user.email == email:
            return False
    
    return True