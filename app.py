from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList, ItemCreate
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dave12334'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

db.init_app(app)

api.add_resource(Store, '/api/stores/<string:name>')
api.add_resource(Item, '/api/items/<string:name>')
api.add_resource(ItemCreate, '/api/items')
api.add_resource(ItemList, '/api/items')
api.add_resource(StoreList, '/api/stores')
api.add_resource(UserRegister, '/api/register')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)