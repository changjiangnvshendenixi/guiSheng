from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, NewsPost,OriginPost,ZonghePost

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/news/')
def get_user_news(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.news.order_by(NewsPost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    news = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_news', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_news', page=page+1, _external=True)
    return jsonify({
        'news': [post.to_json() for post in news],
		'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/users/<int:id>/origin/')
def get_user_origin(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.origin.order_by(OriginPost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    origin = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_origin', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_origin', page=page+1, _external=True)
    return jsonify({
        'origin': [post.to_json() for post in origin],
        'prev': prev,
        'next': next,
        'count': pagination.total
	})


@api.route('/users/<int:id>/zonghe/')
def get_user_zonghe(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.zonghe.order_by(ZonghePost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    zonghe = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_zonghe', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_zonghe', page=page+1, _external=True)
    return jsonify({
        'zonghe': [post.to_json() for post in zonghe],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
