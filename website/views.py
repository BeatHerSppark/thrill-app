from flask import (Blueprint, render_template, flash, g, redirect, request, url_for)
from werkzeug.exceptions import abort

from website.auth import login_required
from website.db import get_db

from .auth import login_required
from .db import get_db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    db  = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('home.html', posts=posts)


@views.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('views.home'))
        
    return render_template('create.html')