from project import app
from flask import render_template, jsonify, request, abort
from project.models import User
from project.auth.jwt_api import JWT_API
from project.auth.wrapers import require_auth

@app.route('/profile', methods=['GET'])
@require_auth
def profile(token):
    try:
        user_id = token['data'].get('user_id')
        user = User.query.filter_by(id=user_id).one_or_none()
        if(user):
            return jsonify({
                'user_id':user.id,
                'user_name':user.user_name,
                'success':True
            })
    except:
        abort(400)