from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
import math

from eapp import admin
from eapp import app, dao, login, utils
from eapp.dao import add_user


@app.route('/')
def index():
    categories = dao.load_categories()

    products = dao.load_products(cate_id=request.args.get('category_id'),
                                 kw=request.args.get('kw'),
                                 page=int(request.args.get('page', 1)))
    return render_template('index.html', products=products,
                           pages=math.ceil(dao.count_products()/app.config['PAGE_SIZE']))

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    data = request.form
    password = data.get('password')
    confirm = data.get('confirm')
    if password != confirm:
        err_msg = "Mật khẩu không đúng. Vui lòng nhập lại!"
        return render_template('register.html', err_msg=err_msg)
    avatar = request.files.get('avatar')
    try:
        add_user(name=data.get('name'), username=data.get('username'), password=password, avatar=request.files.get('avatar'))
        return redirect('/login')
    except Exception as ex:
        return render_template('register.html', err_msg=str(ex))

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    next = request.args.get('next')
    return redirect(next if next else '/admin')

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = str(request.json.get('name'))
        price = str(request.json.get('price'))
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }
    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))

@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories()
    }

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)

if __name__ == '__main__':
    app.run(debug=True)
