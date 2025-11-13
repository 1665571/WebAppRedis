import redis

def initialize_products(redis_client):
    # Lista de productos con todos los campos requeridos
    productos = [
        {"id": 1, "name": "Camiseta", "price": 19.99, "description": "Camiseta de algodón", "stock": 50},
        {"id": 2, "name": "Pantalón", "price": 29.99, "description": "Pantalón vaquero", "stock": 40},
        {"id": 3, "name": "Zapatos", "price": 49.99, "description": "Zapatos de cuero", "stock": 30},
        {"id": 4, "name": "Gorra", "price": 14.99, "description": "Gorra deportiva", "stock": 60},
        {"id": 5, "name": "Chaqueta", "price": 89.99, "description": "Chaqueta impermeable", "stock": 20},
        {"id": 6, "name": "Calcetines", "price": 5.99, "description": "Pack de 3 pares", "stock": 100},
        {"id": 7, "name": "Bufanda", "price": 12.99, "description": "Bufanda de lana", "stock": 35},
        {"id": 8, "name": "Guantes", "price": 9.99, "description": "Guantes térmicos", "stock": 45},
        {"id": 9, "name": "Sudadera", "price": 39.99, "description": "Sudadera con capucha", "stock": 25},
        {"id": 10, "name": "Reloj", "price": 99.99, "description": "Reloj digital", "stock": 15}
    ]

    # Cargar productos en Redis como hashes
    for producto in productos:
        key = f"product:{producto['id']}"
        redis_client.hset(key, mapping={
            "id": producto["id"],
            "name": producto["name"],
            "price": producto["price"],
            "description": producto["description"],
            "stock": producto["stock"]
        })


if __name__ == "__main__":
    try:
        # Conexión a Redis local
        redis_client = redis.Redis(host='redis-plab3-vpdy0u.serverless.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True, ssl=True)

        # Inicializa los productos en Redis
        initialize_products(redis_client)
        print("¡Productos inicializados en Redis!")

    except Exception as e:
        print(f"Error al conectarse a Redis: {e}")
