from flask import Flask, jsonify, request
import mysql.connector
import requests

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(host="mysql_db", user="root", password="rootpassword", database="ecomm_db")

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    
    # 1. Fetch Cart
    cart_resp = requests.get(f'http://cart:5002/cart/{user_id}')
    cart_items = cart_resp.json()
    
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    # 2. Deduct Stock for each item
    for item in cart_items:
        stock_resp = requests.post(f'http://catalog:5001/products/{item["product_id"]}/deduct', 
                                   json={"quantity": item["quantity"]})
        if stock_resp.status_code != 200:
            return jsonify({"error": f"Failed to deduct stock for product {item['product_id']}"}), 400

    # 3. Create Order
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, status) VALUES (%s, %s)", (user_id, 'Pending'))
    conn.commit()
    conn.close()

    # 4. Clear Cart
    requests.delete(f'http://cart:5002/cart/{user_id}')
    
    return jsonify({"message": "Order placed successfully!"}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders)

@app.route('/orders/<int:order_id>/approve', methods=['POST'])
def approve_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status='Processed' WHERE id=%s", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order processed"}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5003)      