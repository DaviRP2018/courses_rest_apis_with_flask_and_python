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

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?;"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?);"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    # @jwt_required()
    def get(self, name):
        try:
            item = self.find_by_name(name)
        except Exception as err:
            return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500
        else:
            if item:
                return item
            return {"message": "Item not found"}, 404

    # @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except Exception as err:
            return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500

        return item, 201

    # @jwt_required()
    def delete(self, name):
        if not self.find_by_name(name):
            return {"message": "Item already deleted."}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?;"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

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
