from .db import db

user_collection = db['users']

def get_user_login(username, password):
    user = user_collection.find_one({'username': username, 'password': password})
    return user