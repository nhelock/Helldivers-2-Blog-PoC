from flask import Flask, render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import os

app = Flask(__name__)

# Initialize Firebase with your service account
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    # Get all blog posts from Firebase
    posts_ref = db.collection('posts').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    
    posts = []
    for doc in posts_ref:
        post_data = doc.to_dict()
        post_data['id'] = doc.id
        posts.append(post_data)
    
    return render_template('home.html', posts=posts)

@app.route('/post/<post_id>')
def view_post(post_id):
    doc = db.collection('posts').document(post_id).get()
    if doc.exists:
        post = doc.to_dict()
        post['id'] = doc.id
        return render_template('post.html', post=post)
    return "Post not found", 404

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        db.collection('posts').add({
            'title': title,
            'content': content,
            'timestamp': datetime.now()
        })
        
        return redirect(url_for('home'))
    
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)