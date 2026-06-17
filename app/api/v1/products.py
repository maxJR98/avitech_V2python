from flask import jsonify, request
from app.api.v1 import v1_bp
from app.models import Product, Stock, Branch
from app.extensions import db

@v1_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.filter_by(is_active=True).all()
    result = [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'category': p.category,
        'image_url': p.image_url
    } for p in products]
    return jsonify(result)

@v1_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'image_url': product.image_url
    })

@v1_bp.route('/products/<int:product_id>/stock', methods=['GET'])
def get_product_stock(product_id):
    branch_id = request.args.get('branch_id', type=int)
    if branch_id:
        stock = Stock.query.filter_by(product_id=product_id, branch_id=branch_id).first()
        quantity = stock.quantity if stock else 0
        return jsonify({'product_id': product_id, 'branch_id': branch_id, 'quantity': quantity})
    stocks = Stock.query.filter_by(product_id=product_id).all()
    result = [{'branch_id': s.branch_id, 'branch_name': s.branch.name, 'quantity': s.quantity} for s in stocks]
    return jsonify(result)