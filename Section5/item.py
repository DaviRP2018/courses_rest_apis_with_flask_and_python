import sqlite3
from flask_restful import Resource, reqparse


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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?;"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}
        return {"message": "Item not found"}, 404

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
