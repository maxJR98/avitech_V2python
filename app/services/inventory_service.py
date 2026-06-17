from app.extensions import db
from app.models import Stock

def check_stock(product_id, branch_id, quantity=1):
    stock = Stock.query.filter_by(product_id=product_id, branch_id=branch_id).first()
    return stock and stock.quantity >= quantity

def reserve_stock(product_id, branch_id, quantity):
    with db.session.begin_nested():
        stock = Stock.query.filter_by(product_id=product_id, branch_id=branch_id).with_for_update().first()
        if not stock or stock.quantity < quantity:
            return False
        stock.quantity -= quantity
        db.session.add(stock)
    db.session.commit()
    return True

def release_stock(product_id, branch_id, quantity):
    with db.session.begin_nested():
        stock = Stock.query.filter_by(product_id=product_id, branch_id=branch_id).with_for_update().first()
        if not stock:
            stock = Stock(product_id=product_id, branch_id=branch_id, quantity=0)
        stock.quantity += quantity
        db.session.add(stock)
    db.session.commit()
    return True