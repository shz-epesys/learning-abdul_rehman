from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.User import User
from handlers.DBHandler import (delete, insert, select, update, delete)
from forms.UserForm import UserSchema, LoginForm, SignupForm
import uuid  # for public id
# from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mars:Mars12345@localhost/lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '77eb7d82c7a65a416b1fb5403c6c33c2'

dotenv_path = '.env'
load_dotenv(dotenv_path)

db = SQLAlchemy(app)
ma = Marshmallow(app)


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = select(
                table='User',
                feilds=[],
                where=f"public_id='{data['public_id']}';"
            )
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_user, *args, **kwargs)
    return decorated


# login
@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(data=request.json)
    if form.validate():
        user_data = select(
            table="User",
            feilds=[],
            where=f'(username="{form.username.data}" or email="{form.username.data}") and password="{form.password.data}"'
        )
        public_id = [user_data1['public_id'] for user_data1 in user_data]
        if public_id:
            token = jwt.encode(
                {
                    'public_id': public_id[0],
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                },
                app.config['SECRET_KEY']
            )
            return make_response(
                jsonify(
                    {
                        'token': token.decode('UTF-8')
                    }
                ),
                201
            )
        else:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )
    return make_response(
        'Could not verify',
        401,
        {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
    )


# Sign  up

@app.route('/signup', methods=['POST'])
def signup():
    form = SignupForm(data=request.json)
    user_data = select(
        table="User",
        feilds=[],
        where=f'username="{form.username.data}" or email="{form.email.data}"'
    )
    print(request.json)
    if form.validate():
        if len(user_data.fetchall()):
            return jsonify({'message': 'User already exits!'}), 406

        else:
            public_id = str(uuid.uuid4())
            insert(
                table='User',
                feilds=['public_id', 'username', 'email', 'password', 'first_name',
                        'last_name', 'contact_no',  'address', 'city'],
                values=[public_id, form.username.data, form.email.data, form.password.data, form.first_name.data,
                        form.last_name.data, form.contact_no.data,  form.address.data, form.city.data]
            )
    else:
        return jsonify({'message': 'Entries not valid!'}), 406
    return jsonify({'message': "Signup successful."}), 201


# Get all Users


@ app.route("/user", methods=['GET'])
@token_required
def get_all_users(current_user):
    all_Users = select("User", [])
    output = []
    for user in all_Users:
        output.append({
            'public_id': user.public_id,
            'name': user.username,
            'email': user.email
        })
    return jsonify({'users': output})

# Get a particular User


@ app.route("/user/<id>", methods=['GET'])
@token_required
def get_profile(current_user, id):
    # init schema
    user_schema = UserSchema()
    user = select("User", [], f' id="{id}"')
    result = user_schema.dump(user.fetchone())
    return jsonify(result)

# update a User


@ app.route('/user/<id>', methods=['PUT'])
@token_required
def update_profile(current_user, id):
    # init schema
    user_schema = UserSchema()
    body = request.json
    user = User(**body)
    user_data = select("User", [], f' id="{id}"')
    status, message = user.validate()
    if status:
        pass
    else:
        return jsonify({'message': message}), 406

    update('User', ['username', 'email', 'password', 'first_name', 'last_name', 'contact_no',  'address', 'city'], [
           user.username, user.email, user.password, user.first_name, user.last_name, user.contact_no,  user.address, user.city], f'id="{id}"')

    result = user_schema.dump(user_data.fetchone())
    return jsonify(result)

# Delete a particular User


@ app.route("/user/<id>", methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    # init schema
    user_schema = UserSchema()
    user_data = select("User", [], f'id="{id}"')
    result = user_schema.dump(user_data.fetchone())
    delete("User", f'id="{id}"')
    return jsonify(result)


# run server
if __name__ == "__main__":
    app.run(debug=True)
