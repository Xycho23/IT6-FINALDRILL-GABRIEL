from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "PHW#84#jeor"
app.config["MYSQL_DB"] = "datasets"
app.config["MYSQL_HOST"] = "localhost"  
app.config["MYSQL_PORT"] = 3306         
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Helper function to fetch data
def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data

# Search endpoints for each table
@app.route("/users/search", methods=["GET"])
def search_users():
    user_id = request.args.get('id')
    if user_id is None:
        return jsonify({'message': 'Missing id parameter'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route("/orders/search", methods=["GET"])
def search_orders():
    order_id = request.args.get('id')
    if order_id is None:
        return jsonify({'message': 'Missing id parameter'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route("/products/search", methods=["GET"])
def search_products():
    product_id = request.args.get('id')
    if product_id is None:
        return jsonify({'message': 'Missing id parameter'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route("/supplier/search", methods=["GET"])
def search_supplier():
    supplier_id = request.args.get('id')
    if supplier_id is None:
        return jsonify({'message': 'Missing id parameter'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supplier WHERE id = %s", (supplier_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Supplier not found'}), 404

@app.route("/total_sales/search", methods=["GET"])
def search_total_sales():
    sales_id = request.args.get('id')
    if sales_id is None:
        return jsonify({'message': 'Missing id parameter'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM total_sales WHERE id = %s", (sales_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Total sales record not found'}), 404

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

# USING INNER JOIN
@app.route('/users/<int:id>/orders', methods=['GET'])
def get_user_orders(id):
    query = """
    SELECT users.name AS user_name, products.name AS product_name, orders.order_date
    FROM users
    INNER JOIN orders ON users.id = orders.user_id
    INNER JOIN products ON orders.product_id = products.id
    WHERE users.id = %s
    """
    data = data_fetch(query, (id,))
    return make_response(jsonify({"users_id": id, "count": len(data), "orders": data}), 200)


#CREATE/UPDATE
@app.route("/users", methods=["POST"])
def create_users():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not all([name, email, age]):
        return jsonify({'message': 'Missing required fields'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    mysql.connection.commit()
    user_id = cur.lastrowid  # Get the ID of the last inserted row
    cur.close()
    created_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }
    return jsonify({'message': 'User added successfully', 'user': created_user}), 201
# CRUD endpoints for users table
@app.route("/users", methods=["GET"])
def get_users():
    data = data_fetch("SELECT * FROM users")
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

#UPDATE
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
    data = data_fetch("SELECT * FROM orders")
    return make_response(jsonify(data), 200)

# CRUD endpoints for products table
@app.route("/products", methods=["GET"])
def get_products():
    data = data_fetch("SELECT * FROM products")
    return make_response(jsonify(data), 200)

# CRUD endpoints for supplier table
@app.route("/supplier", methods=["GET"])
def get_supplier():
    data = data_fetch("SELECT * FROM supplier")
    return make_response(jsonify(data), 200)

# CRUD endpoints for total_sales table
@app.route("/total_sales", methods=["GET"])
def get_total_sales():
    data = data_fetch("SELECT * FROM total_sales")
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
