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

@app.route('/articles/<int:id>')
def show_article(id):
    # Set initial value to 0 if 'page_views' not in session
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the value of session['page_views'] by 1
    session['page_views'] += 1
    
    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        # Fetch the article data based on the provided ID
        article = Article.query.filter_by(id=id).first()
        
        # Check if the article exists
        if article:
            # Render a JSON response with the article data
            return jsonify({'article':article.to_dict()})
        else:
            # If the article with the provided ID does not exist, return a 404 Not Found response
            return {'message': '404: Article not found'}, 404
    else:
        # If the user has viewed more than 3 pages, render a JSON response with an error message
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
