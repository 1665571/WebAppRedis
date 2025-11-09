import redis

def initialize_products(redis_client):
    #TODO: carga 10 productos a la base de datos en AWS.


if __name__ == "__main__":
    try:
        #TODO: Configura la conexión a Redis 
        #redis_client = redis_client es el objeto de conexión a Redis

        # Inicializa los productos en Redis
        initialize_products(redis_client)
        print("¡Productos inicializados en Redis!")

    except Exception as e:
        print(f"Error al conectarse a Redis: {e}")
