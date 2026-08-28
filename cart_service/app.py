from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(host="mysql", user="root", password="rootpassword", database="ecomm_db")

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart_items WHERE user_id=%s", (user_id,))
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)", 
                   (data['user_id'], data['product_id'], data.get('quantity', 1)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Added to cart"}), 201

@app.route('/cart/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE user_id=%s", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Cart cleared"}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5002)