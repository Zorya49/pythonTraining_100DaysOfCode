from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from werkzeug.utils import secure_filename
from .models import Product
from .extensions import db
from .forms import AddProductForm
import os
import math
import stripe

main = Blueprint('main', __name__)

PRODUCTS_PER_PAGE = 12
stripe.api_key = os.environ['STRIPE_API_KEY']


@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@main.route('/products')
def product_list():
    available_products = Product.query.where(Product.stock > 0).all()

    page = request.args.get('page', 1, type=int)

    total_pages = math.ceil(len(available_products) / PRODUCTS_PER_PAGE)

    start_idx = (page - 1) * PRODUCTS_PER_PAGE
    end_idx = start_idx + PRODUCTS_PER_PAGE

    products_on_page = available_products[start_idx:end_idx]
    return render_template('products.html', products=products_on_page, page=page, total_pages=total_pages, current_user=current_user)


@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.where(Product.id == product_id).first()
    if product is None:
        return redirect(url_for('main.product_list'))

    related_products = Product.query.order_by(func.random()).limit(4).all()

    return render_template('product.html', product=product, related_products=related_products, current_user=current_user)


@main.route('/cart')
@login_required
def cart():
    total = 0
    if 'cart' not in session:
        session['cart'] = []
    else:
        for d in session['cart']:
            total = total + d['price'] * d['quantity']
    return render_template('cart.html', cart_items=session['cart'], total=total, current_user=current_user)


@main.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        product = Product.query.where(Product.id == product_id).first()

        # Ensure the product exists and stock is sufficient
        if not product:
            flash(f"Product not found.", 'danger')
            return redirect(url_for('main.product_detail', product_id=product_id))

        if 'cart' in session:
            # Check if the product is already in the cart
            if not any(d['product_id'] == product_id for d in session['cart']) and product.stock >= quantity:
                # Add the product with its details to the cart
                session['cart'].append({
                    'product_id': product_id,
                    'product_name': product.name,
                    'quantity': quantity,
                    'price': product.price
                })
            elif any(d['product_id'] == product_id for d in session['cart']) and product.stock >= quantity:
                # Update the quantity of the product in the cart
                for d in session['cart']:
                    if d['product_id'] == product_id:
                        d['quantity'] = quantity  # Update the quantity
            else:
                flash(f"Requested quantity is higher than current stock.", 'danger')
                return redirect(url_for('main.product_detail', product_id=product_id))
        else:
            # Initialize the cart and add the first product with details
            session['cart'] = [{
                'product_id': product_id,
                'product_name': product.name,
                'quantity': quantity,
                'price': product.price
            }]

        session.modified = True

    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        print(f"Error adding to cart: {e}")

    return redirect(url_for('main.product_detail', product_id=product_id))


@main.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    items = []
    for d in session['cart']:
        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': d['product_name'],
                },
                'unit_amount': int(d['price']*100),
            },
            'quantity': d['quantity'],
        })
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:5000/payment_successful',
            cancel_url='http://127.0.0.1:5000/payment_cancelled',
        )
    except Exception as e:
        return str(e)

    print(checkout_session.url)
    return redirect(checkout_session.url, code=303)


@main.route('/payment_successful')
@login_required
def payment_successful():
    session['cart'] = []
    return render_template('payment_successful.html', current_user=current_user)


@main.route('/payment_cancelled')
@login_required
def payment_cancelled():
    return render_template('payment_cancelled.html', current_user=current_user)


@main.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('main.product_list'))

    form = AddProductForm()
    if form.validate_on_submit():
        existing_product = Product.query.filter_by(name=form.name.data).first()
        if existing_product:
            flash(f"A product with the name '{form.name.data}' already exists.", 'danger')
            return redirect(url_for('main.add_product'))

        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('app/static/uploads', filename)
        image_file.save(image_path)
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            img_src=filename,
            price=form.price.data,
            stock=form.stock.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully.')
        return redirect(url_for('main.administration'))
    else:
        flash('Product details cannot be empty.')
    return render_template('add_product.html', form=form)


@main.route('/admin/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('main.product_list'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    image_path = os.path.join('app/static/uploads', product.img_src)
    os.remove(image_path)
    return redirect(url_for('main.admin'))


@main.route('/admin')
@login_required
def administration():
    if current_user.is_admin:
        products = Product.query.all()
        return render_template('admin.html', products=products, current_user=current_user)
    return redirect(url_for('main.index'))

# TODO: checkout
# @main.route('/checkout')
# @login_required
# def cart():
#     if 'cart' not in session:
#         session['cart'] = []
#     else:
#         total = 0
#         for d in session['cart']:
#             total = total + d['price'] * d['quantity']
#     return render_template('cart.html', cart_items=session['cart'], total=total, current_user=current_user)
#

