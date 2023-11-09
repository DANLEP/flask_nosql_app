from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient(host='db', port=27017)
db = client.mydatabase

@app.route('/items/<key>', methods=['GET', 'PUT'])
def get_or_update_item(key):
    if request.method == 'GET':
        item = db.items.find_one({"key": key})
        if item:
            return jsonify({"key": item["key"], "value": item["value"]})
        else:
            return jsonify({"error": "Item not found"}), 404

    if request.method == 'PUT':
        new_value = request.json.get('value')
        result = db.items.update_one({"key": key}, {"$set": {"value": new_value}})
        if result.modified_count:
            return jsonify({"key": key, "value": new_value})
        else:
            return jsonify({"error": "Item not found or no update made"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    item_data = request.json
    result = db.items.insert_one(item_data)
    return jsonify({"key": item_data["key"], "value": item_data["value"], "id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)