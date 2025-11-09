import redis

def initialize_products(redis_client):
    # Carga 10 productos de ejemplo en Redis
    for i in range(1, 11):
        key = f"product:{i}"
        value = f"Producto {i}"
        redis_client.set(key, value)

if __name__ == "__main__":
    try:
        # Conexión a Redis local
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Inicializa los productos en Redis
        initialize_products(redis_client)
        print("¡Productos inicializados en Redis!")

    except Exception as e:
        print(f"Error al conectarse a Redis: {e}")

