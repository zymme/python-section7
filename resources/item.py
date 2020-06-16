from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be blank!')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='store_id field cannot be blank!')

    @jwt_required()
    def get(self, name):
        print('entered get item by name ' + name)
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'item not found'}, 404

    def delete(self, name):
        print('entered the delete item method for ' + name)
        item = ItemModel.find_by_name(name)
        item.delete_from_db()

        return {'message': 'item successfully deleted'}, 200

    def put(self, name):
        print("entered put method for {}".format(name))
        request_data = Item.parser.parse_args()
        print(request_data)
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
            # item = ItemModel(name, **request_data)

        else:
            item.price = request_data['price']

        item.save_to_db()

        return item.json()


class ItemCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='price field cannot be blank!')
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='name field name cannot be blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='store_id field cannot be blank!')

    def post(self):
        data = ItemCreate.parser.parse_args()
        print(data)
        item = ItemModel.find_by_name(data['name'])

        if item:
            return {'message': "an item with the name '{}' already exists".format(data['name'])}, 400

        item = ItemModel(data['name'], data['price'], data['store_id'])

        try:
            item.save_to_db()
        except Exception:
            return {'message': 'an error occurred inserting the item. '}, 500

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        # return [item.json() for item in ItemModel.query.all()]
        return list(map(lambda x: x.json(), ItemModel.query.all()))
