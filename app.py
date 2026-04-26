from flask import Flask, render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import os
from dotenv import load_dotenv
import markdown
from markupsafe import Markup

load_dotenv()
app = Flask(__name__)

# Initialize Firebase with your service account
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    # Show Updates category posts
    posts_ref = db.collection('posts').where('category', '==', 'updates').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    
    return render_template('home.html', posts=posts, active_page='updates')



@app.route('/post/<post_id>')
def view_post(post_id):
    doc = db.collection('posts').document(post_id).get()
    if doc.exists:
        post = doc.to_dict()
        post['id'] = doc.id
        
        # Convert markdown to HTML
        html_content = markdown.markdown(post['content'])
        post['content_html'] = Markup(html_content)  # Mark as safe HTML
        
        return render_template('post.html', post=post)
    return "Post not found", 404


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    # Get admin secret from URL parameter
    admin_key = request.args.get('admin')
    
    # Get the secret from .env file
    secret = os.getenv('ADMIN_SECRET')
    
    # Check if admin key matches
    if not admin_key or admin_key != secret:
        return "Access Denied. This area is for administrators only.", 401
    
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form.get('subtitle', '')  # Get subtitle, default to empty string if not provided
        content = request.form['content']
        category = request.form['category']
        
        # Add post to Firebase
        db.collection('posts').add({
            'title': title,
            'subtitle': subtitle,  # Add subtitle field
            'content': content,
            'category': category,
            'timestamp': datetime.now()
        })
        
        return redirect(url_for('home'))
    
    # GET request - show the create post form
    return render_template('create.html')



# @app.route('/debug-posts')
# def debug_posts():
#     # Get ALL posts without any filtering
#     all_posts = db.collection('posts').stream()
    
#     result = []
#     for doc in all_posts:
#         data = doc.to_dict()
#         result.append({
#             'id': doc.id,
#             'title': data.get('title'),
#             'category': data.get('category'),
#             'category_type': type(data.get('category')).__name__,
#             'category_length': len(data.get('category', '')),
#             'has_timestamp': 'timestamp' in data
#         })
    
#     from flask import jsonify
#     return jsonify(result)


@app.route('/category/updates')
def category_updates():
    posts_ref = db.collection('posts').where('category', '==', 'updates').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='updates')

@app.route('/category/announcements')
def category_announcements():
    posts_ref = db.collection('posts').where('category', '==', 'announcements').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='announcements')

@app.route('/category/balancing')
def category_balancing():
    posts_ref = db.collection('posts').where('category', '==', 'balancing').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='balancing')

@app.route('/category/story')
def category_story():
    posts_ref = db.collection('posts').where('category', '==', 'story').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='story')

@app.route('/category/surveys')
def category_surveys():
    posts_ref = db.collection('posts').where('category', '==', 'surveys').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='surveys')

@app.route('/category/issues')
def category_issues():
    posts_ref = db.collection('posts').where('category', '==', 'issues').stream()
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    posts.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return render_template('home.html', posts=posts, active_page='issues')

if __name__ == '__main__':
    app.run(debug=True)