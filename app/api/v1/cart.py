from flask import jsonify, request, session
from flask_login import current_user, login_required
from app.api.v1 import v1_bp
from app.models import Product, Branch
from app.services.inventory_service import check_stock

@v1_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if product:
            branch = Branch.query.get(item['branch_id'])
            subtotal = product.price * item['quantity']
            total += subtotal
            items.append({
                'key': key,
                'product_id': product.id,
                'product_name': product.name,
                'branch_id': branch.id if branch else None,
                'branch_name': branch.name if branch else None,
                'quantity': item['quantity'],
                'unit_price': product.price,
                'subtotal': subtotal
            })
    return jsonify({'items': items, 'total': total})

@v1_bp.route('/cart/add', methods=['POST'])
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
    return jsonify({'message': 'Producto agregado al carrito', 'cart': cart})

@v1_bp.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    key = data.get('key')
    cart = session.get('cart', {})
    if key in cart:
        del cart[key]
        session['cart'] = cart
        return jsonify({'message': 'Producto eliminado'})
    return jsonify({'error': 'Elemento no encontrado'}), 404

@v1_bp.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    session.pop('cart', None)
    return jsonify({'message': 'Carrito vaciado'})