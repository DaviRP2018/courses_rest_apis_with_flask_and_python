from flask import Flask
from flask_jwt import JWT
from flask_restful import Resource, Api, reqparse

from Section5.security import authenticate, identity
from Section5.settings import DEBUG
from Section5.user import UserRegister

app = Flask(__name__)
app.secret_key = "Davi"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank!",
    )

    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name '{name}' already exists."}, 400
        # data = request.get_json(force=True)  # force: ignore header Content-Type and try to format to json
        # data = request.get_json(silent=True)  # silent: ignore header Content-Type and return null
        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        # python tries to use the new 'items' variable
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return {"item": item}


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "main":
    app.run(port=5000, debug=DEBUG)
