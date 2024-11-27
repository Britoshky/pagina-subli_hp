from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    categories = [
        {"name": "Books", "url": "/books/"},
        {"name": "Stickers", "url": "/stickers/"},
        {"name": "Cojines", "url": "/cojines/"}
    ]
    return render_template('index.html', categories=categories)
