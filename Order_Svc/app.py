from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory order data
orders = {
    101: {"item": "Laptop", "status": "Pending"},
    102: {"item": "Phone", "status": "Shipped"},
    103: {"item": "Tablet", "status": "Delivered"}
}

# Home route (optional, to avoid 404)
@app.route('/')
def home():
    return "Order Service is Running!"

# GET order details
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({"order_id": order_id, **order})

# UPDATE order status
@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = orders.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    order["status"] = data.get("status", order["status"])

    return jsonify({
        "message": "Order updated successfully",
        "order": {"order_id": order_id, **order}
    })

if __name__ == '__main__':
    app.run(port=5001)