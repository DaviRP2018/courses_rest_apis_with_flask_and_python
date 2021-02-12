from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from Section6.resources.item import Item, ItemList
from Section6.resources.user import UserRegister
from Section6.security import authenticate, identity
from Section6.settings import DEBUG
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Davi"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=DEBUG)
