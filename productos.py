from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Conectar a la base de datos SQLite
def connect_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'db', 'productos.db')
    conn = sqlite3.connect(db_path)
    return conn

# Crear tabla de productos si no existe
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      nombre TEXT, 
                      precio REAL, 
                      descripcion TEXT,
                      categoria TEXT, 
                      stock INTEGER)''')
    conn.commit()
    conn.close()

# Endpoint para agregar un nuevo producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    nuevo_producto = request.json
    nombre = nuevo_producto['nombre']
    precio = nuevo_producto['precio']
    descripcion = nuevo_producto.get('descripcion', '')  # Descripción opcional
    categoria = nuevo_producto.get('categoria', 'General')  # Categoría opcional
    stock = nuevo_producto['stock']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, descripcion, categoria, stock) VALUES (?, ?, ?, ?, ?)", 
                   (nombre, precio, descripcion, categoria, stock))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Producto creado exitosamente'}), 201

# Endpoint para obtener todos los productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

# Endpoint para actualizar un producto
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto_actualizado = request.json
    nombre = producto_actualizado.get('nombre')
    precio = producto_actualizado.get('precio')
    descripcion = producto_actualizado.get('descripcion', '')
    categoria = producto_actualizado.get('categoria', 'General')
    stock = producto_actualizado.get('stock')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''UPDATE productos SET nombre = ?, precio = ?, descripcion = ?, categoria = ?, stock = ? 
                      WHERE id = ?''', 
                   (nombre, precio, descripcion, categoria, stock, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Producto actualizado exitosamente'}), 200

# Endpoint para eliminar un producto
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Producto eliminado exitosamente'}), 200

if __name__ == '__main__':
    create_table()
    app.run(port=8001, debug=True)
