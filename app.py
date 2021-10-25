from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.User import User
from handlers.DBHandler import (delete, insert,select,update,delete)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mars:Mars12345@localhost/lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dotenv_path = '.env'
load_dotenv(dotenv_path)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'contact_no', 'address', 'city')

# create a User
@app.route('/User', methods=['POST'])
def add_User():
    # init schema
    user_schema = UserSchema()
    body = request.json
    user = User(**body)
    status, message = user.validate()
    if status:
        pass
    else:
        return jsonify({'message': message}), 406
 
    insert('User', ['username', 'email','password' ,'first_name', 'last_name', 'contact_no',  'address', 'city'], [user.username,user.email,user.password ,user.first_name, user.last_name, user.contact_no,  user.address, user.city])
    
    user_data = select("User",[],f'username="{user.username}"')

    result = user_schema.dump(*user_data)
    return jsonify(result)


# Get all Users
@app.route("/User", methods=['GET'])
def get_all_users():
    # init schema
    users_schema = UserSchema(many=True)
    all_Users = select("User",[])   
    result = users_schema.dump(all_Users.fetchall())
    return jsonify(result)

# Get a particular User
@app.route("/User/<id>", methods=['GET'])
def get_user(id):
    # init schema
    user_schema = UserSchema()
    user = select("User",[],f' id="{id}"')
    result = user_schema.dump(user.fetchone())
    return jsonify(result)

# update a User
@app.route('/User/<id>', methods=['PUT'])
def update_User(id):
    # init schema
    user_schema = UserSchema()
    body = request.json
    user = User(**body)
    user_data = select("User",[],f' id="{id}"')
    status, message = user.validate()
    if status:
        pass
    else:
        return jsonify({'message': message}), 406

    update('User', ['username', 'email','password' ,'first_name', 'last_name', 'contact_no',  'address', 'city'], [user.username,user.email,user.password ,user.first_name, user.last_name, user.contact_no,  user.address, user.city],f'id="{id}"')

    result = user_schema.dump(user_data.fetchone())
    return jsonify(result)

# Delete a particular User
@app.route("/User/<id>", methods=['DELETE'])
def delete_User(id):
    # init schema
    user_schema = UserSchema()
    user_data = select("User",[],f'id="{id}"')
    result = user_schema.dump(user_data.fetchone())
    delete("User",f'id="{id}"')
    return jsonify(result)


# run server
if __name__ == "__main__":
    app.run(debug=True)

