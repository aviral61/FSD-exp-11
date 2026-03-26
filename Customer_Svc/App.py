from flask import Flask, jsonify
import requests
import os   # ✅ required for Render

app = Flask(__name__)

customers = {
    1: {"name": "Aviral", "orders": [101, 102]},
    2: {"name": "Arvind", "orders": [103]}
}

# ⚠️ CHANGE THIS AFTER DEPLOYMENT
# Replace with your Render Order Service URL
ORDER_SERVICE_URL = "https://your-order-service.onrender.com/order"

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

# ✅ Render-compatible run config
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
