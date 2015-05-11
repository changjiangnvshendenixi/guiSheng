from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import NewsPost,OriginPost,ZonghePost, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden

#------------------------------------------------------------------------------
@api.route('/news/')
def get_news():
    page = request.args.get('page', 1, type=int)
    pagination = NewsPost.query.paginate(
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

@api.route('/origin/')
def get_origin():
    page = request.args.get('page', 1, type=int)
    pagination = OriginPost.query.paginate(
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


@api.route('/zonghe/')
def get_zonghe():
    page = request.args.get('page', 1, type=int)
    pagination = ZonghePost.query.paginate(
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
#-----------------------------------------------------------------------------
@api.route('/news/<int:id>')
def get_news_id(id):
    post = NewsPost.query.get_or_404(id)
    return jsonify(post.to_json())

@api.route('/origin/<int:id>')
def get_origin_id(id):
	post = OriginPost.query.get_or_404(id)
	return jsonify(post.to_json())

@api.route('/zonghe/<int:id>')
def get_zonghe_id(id):
	post = ZonghePost.query.get_or_404(id)
	return jsonify(post.to_json())
#-----------------------------------------------------------------------------

@api.route('/news/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_news():
    post = NewsPost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}

@api.route('/origin/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_origin():
    post = OriginPost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}

@api.route('/zonghe/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_zonghe():
    post = ZonghePost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}
#------------------------------------------------------------------------------

@api.route('/news/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_news(id):
    post = NewsPost.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())

@api.route('/origin/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_origin(id):
    post = OriginPost.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())

@api.route('/zonghe/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_zonghe(id):
    post = ZonghePost.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
#-----------------------------------------------------------------------------
