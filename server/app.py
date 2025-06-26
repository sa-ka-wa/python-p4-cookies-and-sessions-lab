#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([
        {'id': a.id, 'title': a.title, 'content': a.content}
        for a in articles
    ]), 200

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize or increment page views using a ternary
    session['page_views'] = session['page_views'] + 1 if 'page_views' in session else 1

    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'preview': article.content[:50],
            'minutes_to_read':article.minutes_to_read,
            'date': article.date.isoformat()
        }), 200
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    pass

if __name__ == '__main__':
    app.run(port=5555)
