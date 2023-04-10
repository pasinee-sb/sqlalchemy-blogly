"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    return render_template('adduser.html')


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
    tags = Tag.query.all()

    return render_template('addpost.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post(user_id):

    title = request.form['title']
    content = request.form['content']
    # tags = request.form.getlist('tags')
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(post)
    db.session.commit()

    # for tag in tags:
    #     post_tag = PostTag(post_id=post.id, tag_id=tag)
    #     db.session.add(post_tag)

    # db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    tags = post.post_tags

    return render_template('postdetail.html', post=post, my_tags=tags)


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    tags = Tag.query.all()

    post = Post.query.get_or_404(post_id)
    checked_tags = post.post_tags
    return render_template('postedit.html', post=post, tags=tags, checked_tags=checked_tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def show_post_edit(post_id):

    title = request.form['title']
    content = request.form['content']
    # all_post_tags = PostTag.query.all()
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    db.session.commit()

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()

    # tags = request.form.getlist('tags')
    # for tag in tags:
    #     print("SHOW EDIT TAG:" + tag)

    #     for post1 in post.post_tags:
    #         if tag != post1.tags.tag_id:
    #             post_tag = PostTag(post_id=post.id, tag_id=tag)
    #             db.session.add(post_tag)

    db.session.add(post)

    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user_id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user}')


@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tags_detail(tag_id):

    tag = Tag.query.get(tag_id)
    return render_template('tagsdetail.html', tag=tag)


@app.route('/tags/new')
def show_add_tags():
    return render_template('addtag.html')


@app.route('/tags/new', methods=['POST'])
def added_tag():
    tag = request.form['tag']
    tag = Tag(tag_name=tag)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edittag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_edit_tag(tag_id):
    new_tag_name = request.form['tag']
    tag = Tag.query.get(tag_id)
    tag.tag_name = new_tag_name
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):

    Tag.query.filter(Tag.tag_id == tag_id).delete()

    db.session.commit()
    return redirect('/tags')
