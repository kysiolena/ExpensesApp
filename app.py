from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello, I'm your Expense tracking App!")

@app.route("/expense", methods=['POST'])
def create_expense():
    pass

@app.route("/expense", methods=['GET'])
def get_expenses():
    pass

@app.route("/expense/<int:id>", methods=['GET'])
def get_expense(id: int):
    pass

@app.route("/expense/<int:id>", methods=['PATCH'])
def update_expense(id: int):
    pass

@app.route("/expense/<int:id>", methods=['DELETE'])
def delete_expense(id: int):
    pass

if __name__ == "__main__":
    app.run(debug=True)
