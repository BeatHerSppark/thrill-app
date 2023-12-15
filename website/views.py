from flask import Blueprint, render_template

from .auth import login_required
from .db import get_db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')