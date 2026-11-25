import math
from multiprocessing.spawn import set_executable

from flask import render_template, request, redirect, session
from flask_login import login_user, logout_user
from urllib3.util.wait import select_wait_for_socket

from eapp import app, dao, login, utils


@app.route("/")
def index():
    products = dao.load_products(kw=request.args.get('kw'),
                                 cate_id=request.args.get('category_id'),
                                 page=int(request.args.get('page', 1)))
    page_size = app.config['PAGE_SIZE']
    return render_template('index.html', products=products, pages=math.ceil(dao.count_products()/page_size))


@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.authenticate(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    if next:
        return redirect(next)

    return redirect('/admin')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    err_msg = None
    if not password or not confirm or password != confirm:
        err_msg = 'Mật khẩu KHÔNG khớp!'
    else:
        data = request.form.copy()
        del data['confirm']

        avatar = request.files.get('avatar')

        try:
            dao.add_user(**data,avatar=avatar)
            return  redirect('/login')
        except Exception as ex:
            err_msg = str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/logout')
def logout_view():
    logout_user()
    return redirect('/login')

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        cart[id]['quantity']+=1
    else:
        cart[id] = {
            'id': id,
            'name': request.json.get('name'),
            'price': request.json.get('price'),
            'quantity': 1
        }
    session['cart'] = cart
    print(cart)


    return utils.count_cart(cart)

@app.route('/api/carts/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        cart[product_id]['quantity'] = int (request.json.get('quantity',cart[product_id]['quantity']))

        session['cart'] = cart
    return utils.count_cart(cart)

@app.route('/api/carts/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

        session['cart'] = cart
    return utils.count_cart(cart)


@app.context_processor
def common_responses():
    categories = dao.load_categories()

    return {
        'categories': categories,
        'carts': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        from eapp import admin
        app.run(debug=True)
