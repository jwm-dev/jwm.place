from flask import render_template, redirect, url_for, request
from app import app, db, bcrypt
from app.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
import markdown2

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/admin/dashboard')
@login_required
def dashboard():
    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts)

@app.route('/admin/posts', methods=['POST'])
@login_required
def add_post():
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/devlog')
def devlog():
    posts = Post.query.all()
    return render_template('devlog.html', posts=posts)

@app.route('/devlog/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    content = markdown2.markdown(post.content)
    return render_template('post.html', title=post.title, content=content)