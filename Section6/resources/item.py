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
            item.save_to_db()
        except Exception as err:
            return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500

        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": "Item already deleted."}
        item.delete_from_db()
        return {"message": "item deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except Exception as err:
            return {"message": f"An error occurred searching the item.\nError: {err}"}, 500
        else:
            if item is None:
                try:
                    item = ItemModel(name, data["price"])
                    item.save_to_db()
                except Exception as err:
                    return {"message": f"An error occurred inserting the item.\nError: {err}"}, 500
            else:
                try:
                    item.price = data["price"]
                except Exception as err:
                    return {"message": f"An error occurred updating the item.\nError: {err}"}, 500

            return item.json()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # return {"items": list(map(lambda item: item.json(), ItemModel.query.all()))}
