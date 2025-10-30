from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Replace <username> and <password> with your actual Atlas credentials
client = MongoClient("mongodb+srv://manikandan101004_db_user:Changeme123@cluster0.oxz7zii.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.myDatabase  # You can name this whatever you like
users = db.users        # This is your "collection"

@app.route('/')
def home():
    # Example: insert a document
    users.insert_one({"name": "Alice", "age": 25})

    # Fetch data
    data = list(users.find({}, {"_id": 0}))  # remove _id for cleaner output
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
