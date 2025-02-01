from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# Resource: Base class for creating RESTful resources.
# Api: Manages API endpoints.
# reqparse: Parses and validates request arguments.
# fields: Defines the structure of API responses.
# marshal_with: Serializes Python objects into JSON responses.
# abort: Handles errors and returns HTTP error responses.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api=Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, help="Name is required", required=True)
user_args.add_argument("email", type=str, help="Email is required", required=True)

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        result =UserModel.query.all()
        return result
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User not found")
        return result
    
    @marshal_with(userFields)
    def put(self, user_id):
        args = user_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User not found")
        result.name = args['name']
        result.email = args['email']
        db.session.commit()
        return result
    
    @marshal_with(userFields)
    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User not found")
        db.session.delete(result)
        db.session.commit()
        return result, 204

api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:user_id>")
    

    

# Define a route for the home page
@app.route("/")
def home():
    return "Hello, Flask!"

# Define a route for a custom greeting
@app.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)