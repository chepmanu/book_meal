
class User():
    def __init__(self, username, password, email, is_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.id = id(self)

    def to_dict(self):
        return {"username":self.username, "password":self.password, "email":self.email}
      
      
class Order():
    def __init__(self, meal, user):
        self.meal = meal
        self.user = user
        self.id = id(self)

    def to_dict(self):
        return {"user":self.user.to_dict(), "meal":self.meal.to_dict(), "id":self.id} 
      
class Meal():
    def __init__(self, food, price):
        self.food = food
        self.price = price
        self.id = id(self)

    
    def to_dict(self):
        return {"food":self.food, "price":self.price, "id":self.id}

        

order = []
users = []
meals = []
menu = []

orders = []


def verify_email(email):
    for user in users:
        if user.email == email:
            return False
    
    return True