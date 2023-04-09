"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "mimimomo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()


@app.route('/')
def home():

    return redirect('/users')


@app.route('/users')
def list_user():
    """Show list of all users"""
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/users/new')
def add_user():
    """Add user"""
    return render_template('add.html')


@app.route('/users', methods=["POST"])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    """if no image_url entered, get default value from model"""
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show detail of user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts

    # posts = posts.all() if posts else None
    return render_template('userdetail.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def save(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete(user_id):

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('addpost.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post(user_id):

    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('postdetail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('postedit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def show_post_edit(post_id):

    title = request.form['title']
    content = request.form['content']
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user_id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user}')
