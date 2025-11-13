from flask import Flask, render_template, jsonify, request
import redis

app = Flask(__name__)

# Conexión a Redis Serverless
redis_client = redis.Redis(
    host='redis-plab3-vpdy0u.serverless.use1.cache.amazonaws.com',
    port=6379,
    db=0,
    decode_responses=True,
    ssl=True
)

USER_ID = "user1"  # Para pruebas, usar un ID fijo

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = []
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match='product:*', count=100)
        for key in keys:
            products.append(redis_client.hgetall(key))
        cursor = int(cursor)
    return jsonify(products)

@app.route('/cart', methods=['GET'])
def get_cart():
    cart_items = []
    cursor = '0'
    cart_key_prefix = f"cart:{USER_ID}:*"
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match=cart_key_prefix, count=100)
        for key in keys:
            cart_items.append(redis_client.hgetall(key))
        cursor = int(cursor)
    return jsonify(cart_items)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = str(data.get("product_id"))  # <-- Cambiado para JS
    if not product_id:
        return jsonify({"status": "error", "message": "No se especificó product_id"}), 400

    product_key = f"product:{product_id}"
    if not redis_client.exists(product_key):
        return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

    product_data = redis_client.hgetall(product_key)
    cart_item_key = f"cart:{USER_ID}:{product_id}"

    if redis_client.exists(cart_item_key):
        redis_client.hincrby(cart_item_key, "quantity", 1)
    else:
        redis_client.hset(cart_item_key, mapping={
            "id": product_data["id"],
            "name": product_data["name"],
            "price": product_data["price"],
            "quantity": 1
        })

    return jsonify({"status": "added"})

@app.route('/checkout', methods=['POST'])
def checkout():
    cursor = '0'
    cart_key_prefix = f"cart:{USER_ID}:*"
    keys_to_delete = []
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match=cart_key_prefix, count=100)
        keys_to_delete.extend(keys)
        cursor = int(cursor)

    if keys_to_delete:
        redis_client.delete(*keys_to_delete)

    return jsonify({"status": "completed"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
