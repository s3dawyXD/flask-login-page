from . import app
from flask import render_template, jsonify, request, abort
from .models import User
from .auth.jwt_api import JWT_API
from .auth.wrapers import require_auth
from .auth.cryptography_API import cryptography_API


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/users')
@require_auth
def users(w):
    all_users = User.query.all()

    res = {}
    for user in all_users:
        res[user.id] = user.user_name
    return jsonify(res)


@app.route('/login', methods=['POST'])
def login():

    body = request.get_json()
    user_name = body.get('userName')
    password = body.get('password')
    user = User.query.filter_by(user_name=user_name).one_or_none()
    crypto = cryptography_API()
    if(user):
        if(crypto.check_password(user.password, password)):
            j = JWT_API()
            data = {'user_id': user.id}
            token = j.create_jwt(data)
            return jsonify({'jwt': token,
                            'success': True,
                            'message': f'welcome {user_name}'})

    return 'who the hell are you '


@app.route('/register',methods=['POST'])
def register():
    try:
        body = request.get_json()
        user_name = body.get('userName')
        password = body.get('password')
        user = User.query.filter_by(user_name=user_name).one_or_none()
        crypto = cryptography_API()
        if(not user):
            hashed_password = crypto.hash(password=password)
            new_user = User(user_name=user_name, password=hashed_password)
            new_user.insert()
        else:
            return jsonify({
                'success':False,
                'message':'user do exist'
                })
        return jsonify({
            'success':True,
            'message':'user added successfully'
        })
    except:
        abort(400)