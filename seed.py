"""Seed file to make sample data for user db, run on one shell >> python seed.py"""
"""on shell command  >>  createdb blogly """


# Create all tables
import datetime
from models import User, db, Post
from app import app
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
             user_id=2)
db.session.add(post1)
db.session.commit()
