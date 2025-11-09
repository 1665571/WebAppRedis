from flask import Flask, jsonify, request, render_template
import redis

app = Flask(__name__)

# TODO: Configura la conexión a Redis 
#redis_client = redis_client es el objeto de conexión a Redis







@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    
    products = []
    # TODO: Obtener la lista de productos de Redis

    return jsonify(products)

@app.route('/cart', methods=['GET'])
def get_cart():
    
    cart_items = []
    # TODO: Obtener los elementos de la cesta desde Redis


    return jsonify(cart_items)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    # TODO: Añadir un producto a la cesta en Redis con las verificaciones pertinentes
    pass


@app.route('/checkout', methods=['POST'])
def checkout():
    # TODO: Procesar la compra y limpiar la cesta en Redis
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
