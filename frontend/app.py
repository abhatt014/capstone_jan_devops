from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

CATALOG_URL = "http://catalog:5001/products"
CART_URL = "http://cart:5002/cart"
ORDER_URL = "http://order:5003/orders"
USER_ID = 1 # Hardcoded for demonstration

@app.route('/')
def index():
    products = requests.get(CATALOG_URL).json()
    cart = requests.get(f"{CART_URL}/{USER_ID}").json()
    return render_template('index.html', products=products, cart=cart)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    requests.post(CART_URL, json={"user_id": USER_ID, "product_id": product_id, "quantity": 1})
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    resp = requests.post(ORDER_URL, json={"user_id": USER_ID})
    if resp.status_code == 201:
        flash("Order placed successfully!", "success")
    else:
        flash(resp.json().get('error', 'Checkout failed'), "danger")
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    orders = requests.get(ORDER_URL).json()
    return render_template('admin.html', orders=orders)

@app.route('/approve/<int:order_id>')
def approve(order_id):
    requests.post(f"{ORDER_URL}/{order_id}/approve")
    return redirect(url_for('admin'))
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)      