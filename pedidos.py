from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS
import pika
import json
import requests

app = Flask(__name__)
CORS(app)

# Conectar a la base de datos SQLite
def connect_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'db', 'pedidos.db')
    conn = sqlite3.connect(db_path)
    return conn

# Crear tabla de pedidos si no existe
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, cantidad INTEGER)''')
    conn.commit()
    conn.close()

# Función para enviar un mensaje a RabbitMQ
def enviar_mensaje(producto):
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    canal = conexion.channel()
    canal.queue_declare(queue='pedidos_queue')

    mensaje = {
        'producto_id': producto['id'],
        'nombre': producto['nombre'],
        'precio': producto['precio'],
        'cantidad': producto['cantidad']
    }

    canal.basic_publish(exchange='', routing_key='pedidos_queue', body=json.dumps(mensaje))
    print(f"Pedido enviado: {mensaje}")
    conexion.close()

# Función para obtener información de un producto desde el microservicio de productos
def obtener_producto(producto_id):
    try:
        response = requests.get(f"http://localhost:7001/productos/{producto_id}")
        if response.status_code == 200:
            return response.json()  # Devuelve el producto como JSON
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el producto: {e}")
        return None

# Endpoint para crear un nuevo pedido
@app.route('/pedidos', methods=['POST'])
def crear_pedido():
    nuevo_pedido = request.json
    producto_id = nuevo_pedido['producto_id']
    cantidad = nuevo_pedido['cantidad']

    # Obtener información del producto desde el microservicio de productos
    producto = obtener_producto(producto_id)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (producto_id, cantidad) VALUES (?, ?)", (producto_id, cantidad))
    conn.commit()
    conn.close()

    # Enviar información del pedido a RabbitMQ
    producto['cantidad'] = cantidad  # Añadir la cantidad al producto
    enviar_mensaje(producto)

    return jsonify({'message': 'Pedido creado exitosamente'}), 201

# Endpoint para obtener todos los pedidos
@app.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()

    pedidos_con_detalles = []
    for pedido in pedidos:
        pedido_id, producto_id, cantidad = pedido
        producto = obtener_producto(producto_id)
        if producto:
            pedidos_con_detalles.append({
                'pedido_id': pedido_id,
                'producto': producto,
                'cantidad': cantidad
            })

    return jsonify(pedidos_con_detalles)

if __name__ == '__main__':
    create_table()
    app.run(port=8008, debug=True)
