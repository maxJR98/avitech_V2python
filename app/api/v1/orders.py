from flask import jsonify, request, session
from flask_login import current_user, login_required
from app.api.v1 import v1_bp
from app.models import Order, OrderItem, Product, Branch
from app.extensions import db
from app.services.inventory_service import reserve_stock
import uuid

@v1_bp.route('/orders', methods=['GET'])
@login_required
def list_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'date': order.order_date.isoformat(),
            'status': order.status,
            'total': order.total_amount,
            'delivery_type': order.delivery_type,
            'verification_code': order.verification_code
        })
    return jsonify(result)

@v1_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    items = [{
        'product_id': item.product_id,
        'product_name': item.product.name,
        'quantity': item.quantity,
        'unit_price': item.unit_price,
        'subtotal': item.subtotal
    } for item in order.items]
    return jsonify({
        'id': order.id,
        'date': order.order_date.isoformat(),
        'status': order.status,
        'total': order.total_amount,
        'delivery_type': order.delivery_type,
        'branch_id': order.branch_id,
        'verification_code': order.verification_code,
        'items': items
    })

@v1_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    branch_id = data.get('branch_id')
    delivery_type = data.get('delivery_type')  # 'pickup' o 'delivery'
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Carrito vacío'}), 400
    total = 0
    items = []
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({'error': f'Producto {item["product_id"]} no encontrado'}), 400
        subtotal = product.price * item['quantity']
        total += subtotal
        items.append(item)
    order = Order(
        user_id=current_user.id,
        branch_id=branch_id,
        delivery_type=delivery_type,
        total_amount=total,
        shipping_cost=0.0
    )
    if delivery_type == 'pickup':
        order.verification_code = str(uuid.uuid4())[:8].upper()
    db.session.add(order)
    db.session.flush()
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=Product.query.get(item['product_id']).price,
            subtotal=Product.query.get(item['product_id']).price * item['quantity']
        )
        db.session.add(order_item)
        if not reserve_stock(item['product_id'], item['branch_id'], item['quantity']):
            db.session.rollback()
            return jsonify({'error': 'Error al reservar stock'}), 400
    db.session.commit()
    session.pop('cart', None)
    return jsonify({
        'message': 'Pedido creado',
        'order_id': order.id,
        'verification_code': order.verification_code
    }), 201