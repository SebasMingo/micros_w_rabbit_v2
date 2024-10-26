const apiUrlProductos = 'http://localhost:8001/productos';
const apiUrlPedidos = 'http://localhost:8008/pedidos';

function crearProducto() {
    const nombre = document.getElementById('nombreProducto').value;
    const precio = document.getElementById('precioProducto').value;
    const descripcion = document.getElementById('descripcionProducto').value;  // Obtener descripción
    const categoria = document.getElementById('categoriaProducto').value;      // Obtener categoría
    const stock = document.getElementById('stockProducto').value;  // Obtener stock

    fetch(apiUrlProductos, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: nombre, 
            precio: parseFloat(precio), 
            descripcion: descripcion,
            categoria: categoria,
            stock: parseInt(stock)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        listarProductos();
    })
    .catch(error => console.error('Error:', error));
}

function listarProductos() {
    fetch(apiUrlProductos)
    .then(response => response.json())
    .then(data => {
        const productosDiv = document.getElementById('productos');
        productosDiv.innerHTML = '<h2>Lista de Productos:</h2>';
        data.forEach(producto => {
            productosDiv.innerHTML += `
                <div>
                    <p>ID: ${producto[0]}, Nombre: ${producto[1]}, Precio: ${producto[2]}, Stock: ${producto[5]}</p>
                    <p>Descripción: ${producto[3]}, Categoría: ${producto[4]}</p>
                    <button onclick="eliminarProducto(${producto[0]})">Eliminar</button>
                    <button onclick="mostrarFormularioActualizar(${producto[0]}, '${producto[1]}', ${producto[2]}, '${producto[3]}', '${producto[4]}', ${producto[5]})">Actualizar</button>
                </div>
            `;
        });
    })
    .catch(error => console.error('Error:', error));
}

function eliminarProducto(id) {
    fetch(`${apiUrlProductos}/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        listarProductos();
    })
    .catch(error => console.error('Error:', error));
}

function mostrarFormularioActualizar(id, nombre, precio, descripcion, categoria, stock) {
    const productosDiv = document.getElementById('productos');
    productosDiv.innerHTML = `
        <h2>Actualizar Producto:</h2>
        <input type="text" id="nombreProductoActualizar" value="${nombre}">
        <input type="number" id="precioProductoActualizar" value="${precio}">
        <input type="text" id="descripcionProductoActualizar" value="${descripcion}">
        <input type="text" id="categoriaProductoActualizar" value="${categoria}">
        <input type="number" id="stockProductoActualizar" value="${stock}">
        <button onclick="actualizarProducto(${id})">Actualizar Producto</button>
        <button onclick="listarProductos()">Cancelar</button>
    `;
}

function actualizarProducto(id) {
    const nombre = document.getElementById('nombreProductoActualizar').value;
    const precio = document.getElementById('precioProductoActualizar').value;
    const descripcion = document.getElementById('descripcionProductoActualizar').value;
    const categoria = document.getElementById('categoriaProductoActualizar').value;
    const stock = document.getElementById('stockProductoActualizar').value;

    fetch(`${apiUrlProductos}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: nombre,
            precio: parseFloat(precio),
            descripcion: descripcion,
            categoria: categoria,
            stock: parseInt(stock)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        listarProductos();
    })
    .catch(error => console.error('Error:', error));
}

// Llamar a listarProductos y listarPedidos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    listarProductos();
    listarPedidos();
});

function crearPedido() {
    const productos = document.getElementById('productosPedido').value;
    const cantidad = document.getElementById('cantidadPedido').value;

    fetch(apiUrlPedidos, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ producto_id: productos, cantidad: parseInt(cantidad) })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        listarPedidos();
    })
    .catch(error => console.error('Error:', error));
}

function listarPedidos() {
    fetch(apiUrlPedidos)
    .then(response => response.json())
    .then(data => {
        const pedidosDiv = document.getElementById('pedidos');
        pedidosDiv.innerHTML = '<h2>Lista de Pedidos:</h2>';
        data.forEach(pedido => {
            pedidosDiv.innerHTML += `<p>ID: ${pedido[0]}, Productos: ${pedido[1]}, Cantidad: ${pedido[2]}</p>`;
        });
    })
    .catch(error => console.error('Error:', error));
}

// Llamar a listarProductos y listarPedidos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    listarProductos();
    listarPedidos();
});
