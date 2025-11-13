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

# Para este ejemplo asumimos un usuario fijo (en producción usar sesiones o auth)
USER_ID = "user1"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = []
    # Obtener todas las keys de productos
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
    product_id = data.get("id")
    if not product_id:
        return jsonify({"error": "No se especificó product_id"}), 400

    # Verificar que el producto existe en Redis
    product_key = f"product:{product_id}"
    if not redis_client.exists(product_key):
        return jsonify({"error": "Producto no encontrado"}), 404

    product_data = redis_client.hgetall(product_key)

    # Crear o actualizar la entrada en el carrito
    cart_item_key = f"cart:{USER_ID}:{product_id}"
    if redis_client.exists(cart_item_key):
        # Incrementar cantidad
        redis_client.hincrby(cart_item_key, "quantity", 1)
    else:
        # Crear nueva entrada en carrito
        redis_client.hset(cart_item_key, mapping={
            "id": product_data["id"],
            "name": product_data["name"],
            "price": product_data["price"],
            "quantity": 1
        })

    return jsonify({"message": "Producto añadido al carrito"}), 200

@app.route('/checkout', methods=['POST'])
def checkout():
    # Obtener todas las keys del carrito del usuario
    cursor = '0'
    cart_key_prefix = f"cart:{USER_ID}:*"
    keys_to_delete = []
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match=cart_key_prefix, count=100)
        keys_to_delete.extend(keys)
        cursor = int(cursor)

    # Borrar todas las keys del carrito
    if keys_to_delete:
        redis_client.delete(*keys_to_delete)

    return jsonify({"message": "Compra completada y carrito vaciado"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
