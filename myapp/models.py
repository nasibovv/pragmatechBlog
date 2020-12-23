from .__init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKey
from flask_login import AnonymousUserMixin


class userInfo(UserMixin, db.Model):
    __tablename__ = 'userInfo'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200))
    phone = db.Column(db.Integer, unique = True)
    profile_pic = db.Column(db.String(100), default = "img/default.jpeg")

    blog = db.relationship('articles', backref = 'owner')

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    grad_status = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


    def __init__(self, username, password, name, surname, email, phone):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

class articles(db.Model):
    __tablename__ = 'articles'
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(100))
    content = db.Column(db.Text)    
    cover_photo = db.Column(db.String(100))
    likes = db.Column(db.Integer)
    view = db.Column(db.Integer)
    writer_id = db.Column(db.Integer, db.ForeignKey('userInfo.id'))
    read_time = db.Column(db.Integer)

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    active = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, content, cover_photo, likes, view, writer_id, read_time):
        self.title = title
        self.content = content
        self.cover_photo = cover_photo
        self.likes = likes
        self.view = view
        self.writer_id = writer_id
        self.read_time = read_time


class article_tags(db.Model):
    __tablename__ = 'article_tags'

    id = db.Column(db.Integer, primary_key = True)

    article_id = db.Column(db.Integer, ForeignKey('articles.id'))
    tag_id = db.Column(db.Integer, ForeignKey('tags.id'))


class tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
    self.name = 'Guest'
    self.is_admin = 0
    self.profile_pic = ' '