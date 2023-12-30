from flask import (Blueprint, render_template, flash, g, redirect, request, url_for, jsonify)
import json
from .db import get_db

api = Blueprint('api', __name__)


@api.route('/like', methods=['POST'])
def like():
    data = json.loads(request.data)
    db = get_db()
    prevLiked = db.execute(
        'SELECT user_id, post_id'
        ' FROM like WHERE user_id = ? AND post_id = ?', 
        (data['user_id'], data['post_id'])
    ).fetchone()

    if prevLiked is None:
        db.execute(
            'INSERT INTO like (user_id, post_id)'
            ' VALUES (?, ?)',
            (data['user_id'], data['post_id'])
        )
        db.commit()
        return jsonify({'success': 'post liked'})
    else:
        db.execute(
            'DELETE FROM like WHERE user_id = ? AND post_id = ?',
            (data['user_id'], data['post_id'])
        )
        db.commit()
        return jsonify({'success': 'post unliked'})

    
