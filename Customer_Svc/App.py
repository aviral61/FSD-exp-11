from flask import Flask, jsonify
import requests

app = Flask(__name__)

customers = {
    1: {"name": "Aviral", "orders": [101, 102]},
    2: {"name": "Arvind", "orders": [103]}
}

ORDER_SERVICE_URL = "http://localhost:5001/order"

@app.route('/')
def home():
    return "Customer Service Running!"

@app.route('/customer/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = customers.get(customer_id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    orders_data = []

    for order_id in customer["orders"]:
        try:
            response = requests.get(f"{ORDER_SERVICE_URL}/{order_id}")
            if response.status_code == 200:
                orders_data.append(response.json())
        except:
            orders_data.append({"order_id": order_id, "status": "Service unavailable"})

    return jsonify({
        "customer": customer["name"],
        "orders": orders_data
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)