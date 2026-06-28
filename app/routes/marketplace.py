from flask import Blueprint, render_template, jsonify, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
# Actualizamos los modelos a los nombres generados por la base de datos MySQL
from app.models.modelos_db import Productos, Sucursales, InventarioSucursal, Pedidos, DetallePedido
from app.services.inventory_service import check_stock, reserve_stock
from app.services.location_service import get_nearby_branches
import uuid

marketplace_bp = Blueprint('marketplace', __name__, template_folder='../templates/marketplace')

@marketplace_bp.route('/')
def products():
    # Usamos 'activo=1' en lugar de 'is_active=True'
    products = Productos.query.filter_by(activo=1).all()
    branches = Sucursales.query.filter_by(activo=1).all()
    return render_template('products.html', products=products, branches=branches)

@marketplace_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Productos.query.get_or_404(product_id)
    branches = Sucursales.query.filter_by(activo=1).all()
    stock_info = []
    for branch in branches:
        # Usamos InventarioSucursal y sus columnas correspondientes
        stock = InventarioSucursal.query.filter_by(id_producto=product_id, id_sucursal=branch.id_sucursal).first()
        stock_info.append({
            'branch_id': branch.id_sucursal,
            'branch_name': branch.nombre_sucursal,
            'quantity': stock.cantidad_disponible if stock else 0
        })
    return render_template('product_detail.html', product=product, stock_info=stock_info)

@marketplace_bp.route('/api/stock/<int:product_id>/<int:branch_id>')
def api_check_stock(product_id, branch_id):
    quantity = request.args.get('quantity', 1, type=int)
    available = check_stock(product_id, branch_id, quantity)
    return jsonify({'available': available})

@marketplace_bp.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    branch_id = data.get('branch_id')
    quantity = data.get('quantity', 1)
    
    if not product_id or not branch_id:
        return jsonify({'error': 'Faltan datos'}), 400
    if not check_stock(product_id, branch_id, quantity):
        return jsonify({'error': 'Stock insuficiente'}), 400
        
    cart = session.get('cart', {})
    key = f"{product_id}_{branch_id}"
    
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {'product_id': product_id, 'branch_id': branch_id, 'quantity': quantity}
        
    session['cart'] = cart
    return jsonify({'message': 'Producto agregado', 'cart': cart})

@marketplace_bp.route('/api/cart/count')
def cart_count():
    cart = session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return jsonify({'count': count})

@marketplace_bp.route('/cart')
@login_required
def cart():
    cart_data = session.get('cart', {})
    items = []
    total = 0
    for key, item in cart_data.items():
        product = Productos.query.get(item['product_id'])
        if product:
            branch = Sucursales.query.get(item['branch_id'])
            # Usamos precio_unitario en lugar de price
            subtotal = product.precio_unitario * item['quantity']
            total += subtotal
            items.append({
                'key': key,
                'product': product,
                'branch': branch,
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
    return render_template('cart.html', items=items, total=total)

@marketplace_bp.route('/api/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    key = data.get('key')
    cart = session.get('cart', {})
    if key in cart:
        del cart[key]
        session['cart'] = cart
    return jsonify({'message': 'Eliminado'})

@marketplace_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        branch_id = request.form.get('branch_id')
        delivery_type = request.form.get('delivery_type')
        cart = session.get('cart', {})
        
        if not cart:
            flash('El carrito está vacío.', 'danger')
            return redirect(url_for('marketplace.cart'))
            
        total = 0
        items = []
        for key, item in cart.items():
            product = Productos.query.get(item['product_id'])
            if not product:
                continue
            subtotal = product.precio_unitario * item['quantity']
            total += subtotal
            items.append(item)
            
        # Asignar ID de método de entrega basado en la DB (1=Recojo, 2/3=Delivery)
        id_metodo = 1 if delivery_type == 'pickup' else 2
        
        # Generar un número de pedido único requerido por la DB
        num_pedido = f"PED-{str(uuid.uuid4())[:6].upper()}"
        
        order = Pedidos(
            numero_pedido=num_pedido,
            id_cliente=current_user.id_usuario, # Asegúrate de que flask_login use id_usuario
            id_sucursal=branch_id,
            id_estado=1, # 1 = Pendiente según tus seeds
            id_metodo_entrega=id_metodo,
            subtotal=total,
            costo_envio=0.0,
            total=total
        )
        
        if delivery_type == 'pickup':
            order.notas_cliente = f"Código de verificación: {str(uuid.uuid4())[:8].upper()}"
            
        db.session.add(order)
        db.session.flush() # Para obtener el id_pedido generado
        
        for item in items:
            prod = Productos.query.get(item['product_id'])
            order_item = DetallePedido(
                id_pedido=order.id_pedido,
                id_producto=item['product_id'],
                cantidad=item['quantity'],
                precio_unitario=prod.precio_unitario,
                subtotal=prod.precio_unitario * item['quantity']
            )
            db.session.add(order_item)
            
            if not reserve_stock(item['product_id'], item['branch_id'], item['quantity']):
                db.session.rollback()
                flash('Error al reservar stock.', 'danger')
                return redirect(url_for('marketplace.cart'))
                
        db.session.commit()
        session.pop('cart', None)
        flash('Pedido realizado con éxito.', 'success')
        return redirect(url_for('main.dashboard'))
        
    branches = Sucursales.query.filter_by(activo=1).all()
    return render_template('checkout.html', branches=branches)