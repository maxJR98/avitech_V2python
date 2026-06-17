from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.extensions import db
from app.models import User, Product, Branch, Disease, GeneticLine, Order, Stock, GrowthTable
from app.forms import ProductForm, BranchForm, DiseaseForm, GeneticLineForm, GrowthTableForm

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/')
@login_required
@admin_required
def index():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_branches = Branch.query.count()
    total_orders = Order.query.count()
    total_diseases = Disease.query.count()
    total_genetic_lines = GeneticLine.query.count()
    return render_template('admin/index.html',
                           total_users=total_users,
                           total_products=total_products,
                           total_branches=total_branches,
                           total_orders=total_orders,
                           total_diseases=total_diseases,
                           total_genetic_lines=total_genetic_lines)

@admin_bp.route('/products')
@login_required
@admin_required
def list_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image_url=form.image_url.data,
            is_active=form.is_active.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Producto creado con éxito.', 'success')
        return redirect(url_for('admin.list_products'))
    return render_template('admin/product_form.html', form=form, product=None)

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        product.image_url = form.image_url.data
        product.is_active = form.is_active.data
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('admin.list_products'))
    return render_template('admin/product_form.html', form=form, product=product)

@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin.list_products'))

@admin_bp.route('/branches')
@login_required
@admin_required
def list_branches():
    branches = Branch.query.all()
    return render_template('admin/branches.html', branches=branches)

@admin_bp.route('/branches/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_branch():
    form = BranchForm()
    if form.validate_on_submit():
        branch = Branch(
            name=form.name.data,
            address=form.address.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            phone=form.phone.data,
            email=form.email.data,
            is_active=form.is_active.data
        )
        db.session.add(branch)
        db.session.commit()
        flash('Sucursal creada.', 'success')
        return redirect(url_for('admin.list_branches'))
    return render_template('admin/branch_form.html', form=form, branch=None)

@admin_bp.route('/branches/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_branch(id):
    branch = Branch.query.get_or_404(id)
    form = BranchForm(obj=branch)
    if form.validate_on_submit():
        branch.name = form.name.data
        branch.address = form.address.data
        branch.latitude = form.latitude.data
        branch.longitude = form.longitude.data
        branch.phone = form.phone.data
        branch.email = form.email.data
        branch.is_active = form.is_active.data
        db.session.commit()
        flash('Sucursal actualizada.', 'success')
        return redirect(url_for('admin.list_branches'))
    return render_template('admin/branch_form.html', form=form, branch=branch)

@admin_bp.route('/branches/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_branch(id):
    branch = Branch.query.get_or_404(id)
    db.session.delete(branch)
    db.session.commit()
    flash('Sucursal eliminada.', 'success')
    return redirect(url_for('admin.list_branches'))

@admin_bp.route('/diseases')
@login_required
@admin_required
def list_diseases():
    diseases = Disease.query.all()
    return render_template('admin/diseases.html', diseases=diseases)

@admin_bp.route('/diseases/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_disease():
    form = DiseaseForm()
    if form.validate_on_submit():
        disease = Disease(
            name=form.name.data,
            scientific_name=form.scientific_name.data,
            description=form.description.data,
            treatment=form.treatment.data,
            prevention=form.prevention.data,
            keywords=form.keywords.data
        )
        db.session.add(disease)
        db.session.commit()
        flash('Enfermedad creada.', 'success')
        return redirect(url_for('admin.list_diseases'))
    return render_template('admin/disease_form.html', form=form, disease=None)

@admin_bp.route('/diseases/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_disease(id):
    disease = Disease.query.get_or_404(id)
    form = DiseaseForm(obj=disease)
    if form.validate_on_submit():
        disease.name = form.name.data
        disease.scientific_name = form.scientific_name.data
        disease.description = form.description.data
        disease.treatment = form.treatment.data
        disease.prevention = form.prevention.data
        disease.keywords = form.keywords.data
        db.session.commit()
        flash('Enfermedad actualizada.', 'success')
        return redirect(url_for('admin.list_diseases'))
    return render_template('admin/disease_form.html', form=form, disease=disease)

@admin_bp.route('/diseases/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_disease(id):
    disease = Disease.query.get_or_404(id)
    db.session.delete(disease)
    db.session.commit()
    flash('Enfermedad eliminada.', 'success')
    return redirect(url_for('admin.list_diseases'))

@admin_bp.route('/genetic-lines')
@login_required
@admin_required
def list_genetic_lines():
    lines = GeneticLine.query.all()
    return render_template('admin/genetic_lines.html', genetic_lines=lines)

@admin_bp.route('/genetic-lines/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_genetic_line():
    form = GeneticLineForm()
    if form.validate_on_submit():
        line = GeneticLine(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(line)
        db.session.commit()
        flash('Línea genética creada.', 'success')
        return redirect(url_for('admin.list_genetic_lines'))
    return render_template('admin/genetic_line_form.html', form=form, line=None)

@admin_bp.route('/genetic-lines/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_genetic_line(id):
    line = GeneticLine.query.get_or_404(id)
    form = GeneticLineForm(obj=line)
    if form.validate_on_submit():
        line.name = form.name.data
        line.description = form.description.data
        db.session.commit()
        flash('Línea genética actualizada.', 'success')
        return redirect(url_for('admin.list_genetic_lines'))
    return render_template('admin/genetic_line_form.html', form=form, line=line)

@admin_bp.route('/genetic-lines/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_genetic_line(id):
    line = GeneticLine.query.get_or_404(id)
    db.session.delete(line)
    db.session.commit()
    flash('Línea genética eliminada.', 'success')
    return redirect(url_for('admin.list_genetic_lines'))