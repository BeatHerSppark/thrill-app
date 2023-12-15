from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not email:
            error = 'Email is required.'
        elif len(username)<3:
            error = 'Username must be at least 3 characters.'
        elif len(password)<6:
            error = 'Password must be longer than 6 characters.'

        if error is None:
            pass

        flash(error)


    return render_template("register.html")


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "logout"