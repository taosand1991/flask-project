from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import db_session
from flaskr.models.user import Post
from datetime import datetime

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print(session['user_id'])
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, description=body, user_id=session['user_id'])
            db_session.add(post)
            db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# def get_post(id, check_author=True):
#     post = 

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.filter_by(id=id, user_id=session['user_id']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post.query.filter_by(id=id, user_id=session['user_id']).first()
            print(body)
            post.title = title
            post.description = body
            post.user_id = session['user_id']
            post.updated_at = datetime.now()
            db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('blog.index'))