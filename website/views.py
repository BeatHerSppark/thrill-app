import os
from flask import (Blueprint, render_template, flash, g, redirect, request, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from website.auth import login_required
from website.db import get_db
from website import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, create_app

from .auth import login_required
from .db import get_db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    db  = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, image_path, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('home.html', posts=posts)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if 'image' not in request.files:
            flash('No image!')
            return redirect(url_for('views.create'))
        
        image = request.files['image']
        filename = None

        if image.filename == '':
            flash('No image!')
            return redirect(url_for('views.create'))
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(create_app().config['UPLOAD_FOLDER'], filename))
            

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, image_path)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], f"/images/{filename}")
            )
            db.commit()
            return redirect(url_for('views.home'))
        
    return render_template('create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, image_path, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@views.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        oldImage = post['image_path']
        image = None
        filename = None

        if 'image' not in request.files:
            flash('No image!')
            return redirect(url_for('views.edit'))
        
        image = request.files['image']

        if image.filename == '':
            flash('No image!')
            return redirect(url_for('views.edit'))
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            print(os.path.join(create_app().config['UPLOAD_FOLDER'], oldImage[8::]))
            os.remove(os.path.join(create_app().config['UPLOAD_FOLDER'], oldImage[8::]))
            image.save(os.path.join(create_app().config['UPLOAD_FOLDER'], filename))
        else:
            flash('Something went wrong.')
            return redirect(url_for('views.edit'))
        
        db = get_db()
        db.execute(
            'UPDATE post SET title= ?, body = ?, image_path = ?'
            ' WHERE id = ?', (title, body, f"/images/{filename}", id)
        )
        db.commit()
        return redirect(url_for('views.home'))
    
    return render_template('edit.html', post=post)


@views.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    oldImage = post['image_path']
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    os.remove(os.path.join(create_app().config['UPLOAD_FOLDER'], oldImage[8::]))
    return redirect(url_for('views.home'))
