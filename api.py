from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "PHW#84#jeor"
app.config["MYSQL_DB"] = "datasets"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

# CRUD endpoints for users table
@app.route("/users", methods=["GET"])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not all([name, email, age]):
        return jsonify({'message': 'Missing required fields'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User added successfully'}), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not all([name, email, age]):
        return jsonify({'message': 'Missing required fields'}), 400
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s", (name, email, age, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User updated successfully'})

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'})

# CRUD endpoints for orders table
@app.route("/orders", methods=["GET"])
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

# CRUD endpoints for products table
@app.route("/products", methods=["GET"])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

# CRUD endpoints for supplier table
@app.route("/supplier", methods=["GET"])
def get_supplier():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supplier")
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

# CRUD endpoints for total_sales table
@app.route("/total_sales", methods=["GET"])
def get_total_sales():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM total_sales")
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
