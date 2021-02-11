from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from Section4.security import authenticate, identity
from Section4.settings import DEBUG

app = Flask(__name__)
app.secret_key = "Davi"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name '{name}' already exists."}, 400
        # data = request.get_json(force=True)  # force: ignore header Content-Type and try to format to json
        data = request.get_json(silent=True)  # silent: ignore header Content-Type and return null
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        # python tries to use the new 'items' variable
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "main":
    app.run(port=5000, debug=DEBUG)
