from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(host="mysql_db", user="root", password="rootpassword", database="ecomm_db")

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/products/<int:prod_id>/deduct', methods=['POST'])
def deduct_stock(prod_id):
    qty = request.json.get('quantity', 1)
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT stock FROM products WHERE id=%s", (prod_id,))
    product = cursor.fetchone()
    
    if product and product['stock'] >= qty:
        cursor.execute("UPDATE products SET stock = stock - %s WHERE id=%s", (qty, prod_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Stock deducted"}), 200
    
    conn.close()
    return jsonify({"error": "Insufficient stock"}), 400
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)    