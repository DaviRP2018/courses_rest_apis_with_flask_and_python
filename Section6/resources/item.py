import sqlite3

from flask_restful import Resource, reqparse

from Section6.modules.item import ItemModel


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
        try:
            item = ItemModel.find_by_name(name)
        except Exception as err:
            return {"message": f"An error occurred searching the item.\nError: {err}"}, 500
        else:
            if item:
                return item.json()
            return {"message": "Item not found"}, 404

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.insert()
        except Exception as err:
            return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500

        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {"message": "Item already deleted."}

        connection = sqlite3.connect("../data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?;"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "item deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except Exception as err:
            return {"message": f"An error occurred searching the item.\nError: {err}"}, 500
        else:
            updated_item = ItemModel(name, data["price"])

            if item is None:
                try:
                    updated_item.insert()
                except Exception as err:
                    return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500
            else:
                try:
                    updated_item.update()
                except Exception as err:
                    return {"message": f"An error occurred updating the item.\nError: {err}"}, 500

            return updated_item.json()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect("../data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items;"
        result = cursor.execute(query)
        items = [{"name": row[0], "price": row[1]} for row in result]

        connection.close()

        return {"items": items}
