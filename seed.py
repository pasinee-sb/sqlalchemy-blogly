"""Seed file to make sample data for user db, run on one shell >> python seed.py"""
"""on shell command  >>  createdb blogly """


# Create all tables
from app import app
import datetime
from models import User, db, Post, Tag, PostTag
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users

dani = User(first_name='Daniel', last_name='Oh')
minki = User(first_name='Minki', last_name='Bo')
joel = User(first_name='Joel', last_name='Co')


# Add new objects to session, so they'll persist
db.session.add(dani)
db.session.add(minki)
db.session.add(joel)

# Commit--otherwise, this never gets saved!
db.session.commit()

post1 = Post(title='Music', content='Music is life',
             user_id=1)
post2 = Post(title='Travel', content='Travel is life',
             user_id=2)
post3 = Post(title='Hobby', content='Hobby is life',
             user_id=3)
db.session.add_all([post1, post2, post3])
db.session.commit()

goodtag = Tag(tag_name="good")
funnytag = Tag(tag_name="funny")
scarytag = Tag(tag_name="scary")

db.session.add_all([goodtag, funnytag, scarytag])
db.session.commit()

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=2, tag_id=2)
pt3 = PostTag(post_id=3, tag_id=3)
pt4 = PostTag(post_id=1, tag_id=2)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()
