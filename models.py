from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""


class User (db.Model):
    '''User'''
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name = {u.first_name} last_name = {u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String,
                           nullable=False)
    last_name = db.Column(db.String,
                          nullable=False)

    image_url = db.Column(
        db.String, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStvZlb5voYlK89uQ022tB03USKvRGNouLJJw&usqp=CAU')
    posts = db.relationship(
        'Post', cascade="all, delete-orphan")
    # Part Two : Adding posts


class Post(db.Model):

    '''Post'''
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))
    user = db.relationship('User', overlaps="posts")
    # tags = db.relationship('PostTag', overlaps="posts")
    post_tags = db.relationship('PostTag', backref="tag_posts")

    tags = db.relationship('Tag', secondary="post_tag", overlaps="post_tags")

    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"


class Tag (db.Model):
    '''Tag'''
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    tag_name = db.Column(db.Text, unique=True)

    # posts = db.relationship('PostTag', overlaps="tags")
    post_tags = db.relationship('PostTag', backref="tags")

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    posts = db.relationship('Post', secondary="post_tag",
                            overlaps="post_tags,tags")

    def __repr__(self):
        t = self
        return f"<Tag {t.tag_id} {t.tag_name} >"


class PostTag (db.Model):
    '''PostTag'''
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.tag_id'), primary_key=True)

    tag_role = db.Column(db.Text)
