from flask_sqlalchemy import SQLAlchemy
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
