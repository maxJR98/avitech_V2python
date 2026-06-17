import json
from flask import session

def get_cart_total():
    cart = session.get('cart', {})
    total = 0
    from app.models import Product
    for key, item in cart.items():
        product = Product.query.get(item['product_id'])
        if product:
            total += product.price * item['quantity']
    return total

def cart_count():
    cart = session.get('cart', {})
    return sum(item['quantity'] for item in cart.values())