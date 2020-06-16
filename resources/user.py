
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username is a required field')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='password is a required field')

    def post(self):
        print('entered POST for UserRegister ...')
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'That username already exists!'}, 400

        user = UserModel(**data)  # unpacks the dictionary
        user.save_to_db()

        return {'message': 'User successfully created'}, 201
