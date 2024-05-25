from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "PHW#84#jeor"
app.config["MYSQL_DB"] = "datasets"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'admin123'

def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # Dummy check for username and password (use database in production)
    if auth.username == '' and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route("/users/search", methods=["GET"])
@token_required
def search_users(current_user):
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
@token_required
def search_orders(current_user):
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
@token_required
def search_products(current_user):
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
@token_required
def search_supplier(current_user):
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
@token_required
def search_total_sales(current_user):
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

@app.route('/users/<int:id>/orders', methods=['GET'])
@token_required
def get_user_orders(current_user, id):
    query = """
    SELECT users.name AS user_name, products.name AS product_name, orders.order_date
    FROM users
    INNER JOIN orders ON users.id = orders.user_id
    INNER JOIN products ON orders.product_id = products.id
    WHERE users.id = %s
    """
    data = data_fetch(query, (id,))
    return make_response(jsonify({"users_id": id, "count": len(data), "orders": data}), 200)

@app.route("/users", methods=["POST"])
@token_required
def create_users(current_user):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not all([name, email, age]):
        return jsonify({'message': 'Missing required fields'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    mysql.connection.commit()
    user_id = cur.lastrowid
    cur.close()
    created_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }
    return jsonify({'message': 'User added successfully', 'user': created_user}), 201

@app.route("/users/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
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
@token_required
def delete_user(current_user, id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'})

@app.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    data = data_fetch("SELECT * FROM users")
    return make_response(jsonify(data), 200)

@app.route("/orders", methods=["GET"])
@token_required
def get_orders(current_user):
    data = data_fetch("SELECT * FROM orders")
    return make_response(jsonify(data), 200)

@app.route("/products", methods=["GET"])
@token_required
def get_products(current_user):
    data = data_fetch("SELECT * FROM products")
    return make_response(jsonify(data), 200)

@app.route("/supplier", methods=["GET"])
@token_required
def get_supplier(current_user):
    data = data_fetch("SELECT * FROM supplier")
    return make_response(jsonify(data), 200)

@app.route("/total_sales", methods=["GET"])
@token_required
def get_total_sales(current_user):
    data = data_fetch("SELECT * FROM total_sales")
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
