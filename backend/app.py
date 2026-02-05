from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 HOME ROUTE
@app.route('/')
def home():
    return "Emergency Home Service Backend Running with Database!"

# =========================================================
# 👤 CUSTOMER REGISTER
# =========================================================
@app.route('/customer/register', methods=['POST'])
def customer_register():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO customers (name, phone, password) VALUES (?, ?, ?)',
            (name, phone, password)
        )
        conn.commit()
    except:
        return jsonify({"message": "Phone number already registered"}), 400
    finally:
        conn.close()

    return jsonify({"message": "Customer registered successfully"})

    # 🔹 CUSTOMER LOGIN
@app.route('/customer/login', methods=['POST'])
def customer_login():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    conn = get_db_connection()
    customer = conn.execute(
        'SELECT * FROM customers WHERE phone = ? AND password = ?',
        (phone, password)
    ).fetchone()
    conn.close()

    if customer:
        return jsonify({
            "message": "Login successful",
            "customer_id": customer["id"],
            "name": customer["name"]
        })
    else:
        return jsonify({"message": "Invalid phone or password"}), 401

# 🔹 WORKER REGISTER
@app.route('/worker/register', methods=['POST'])
def worker_register():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    service_type = data.get('service_type')
    experience = data.get('experience')

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO workers (name, phone, service_type, experience) VALUES (?, ?, ?, ?)',
            (name, phone, service_type, experience)
        )
        conn.commit()
    except:
        return jsonify({"message": "Phone already registered"}), 400
    finally:
        conn.close()

    return jsonify({"message": "Worker registered. Waiting for approval."})



# =========================================================
# 🛠 BOOK SERVICE (Now linked to customer account)
# =========================================================
@app.route('/book-service', methods=['POST'])
def book_service():
    data = request.get_json()

    customer_id = data.get('customer_id')
    service_type = data.get('service_type')
    address = data.get('address')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO bookings (customer_id, service_type, address, status) VALUES (?, ?, ?, ?)',
        (customer_id, service_type, address, 'Waiting for Worker')
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Service booked successfully!"})

# =========================================================
# 📋 VIEW ALL BOOKINGS
# =========================================================
@app.route('/bookings', methods=['GET'])
def get_bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()

    bookings_list = [dict(booking) for booking in bookings]
    return jsonify(bookings_list)

# 🔹 VIEW ALL WORKERS
@app.route('/workers', methods=['GET'])
def get_workers():
    conn = get_db_connection()
    workers = conn.execute('SELECT id, name, phone, service_type, experience FROM workers').fetchall()
    conn.close()

    workers_list = [dict(worker) for worker in workers]
    return jsonify(workers_list)


# 🔹 RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)
