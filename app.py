from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKey
from sqlalchemy import insert, or_
import os
import random
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from flask_login import AnonymousUserMixin
from form import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login' #?

class userInfo(UserMixin, db.Model):
    __tablename__ = 'userInfo'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200))
    phone = db.Column(db.Integer, unique = True)

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    grad_status = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
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
    writer_id = db.Column(db.Integer, ForeignKey('userInfo.id'))

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, title, content, cover_photo, likes, view):
        self.title = title
        self.content = content
        self.cover_photo = cover_photo
        self.likes = likes
        self.view = view


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

login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    return userInfo.query.get(user_id)

@app.context_processor #to send variable to base.html
def inject_user():
    name = current_user.username
    
    return dict(name = name)


@app.route('/')   
def home():  
    #name = current_user.username

    last_item = articles.query.order_by(articles.id.desc()).first()
    id =  last_item.id
    blog_list = list()
    top_blog_list = list()

    for x in range(2):
        top_blog = articles.query.get(id)
        top_blog_list.append(top_blog)
        id = id - 1

    for x in range(6):
        blog = articles.query.get(id)
        blog_list.append(blog)
        id = id - 1


    last_item2 = tags.query.order_by(tags.id.desc()).first()
    tag_id =  last_item2.id
    tag_list = list()

    rand_id = random.sample(range(1, tag_id + 1), 5)
    for i in range(5):
        tag = tags.query.get(rand_id[i])
        tag_list.append(tag)

    return render_template('index-2.html', recent_blog = blog_list, popular_tag = tag_list, top_blog = top_blog_list)  
 

@app.route('/category')   
def category():  
    return render_template('category.html')  

@app.route('/about')   
def about():  
    return render_template('about.html')  

@app.route('/contact')   
def contact():  
    return render_template('contact.html')  

@app.route('/blog/<int:id>')
def blog(id):

    last_item2 = tags.query.order_by(tags.id.desc()).first()
    tag_id =  last_item2.id
    tag_list = list()

    last_item = articles.query.order_by(articles.id.desc()).first()
    id_rec =  last_item.id
    blog_list = list()

    for x in range(4):
        blog = articles.query.get(id_rec)
        blog_list.append(blog)
        id_rec = id_rec - 1

    next_prev_blog = list()

    prev = articles.query.get(id-1)
    _next = articles.query.get(id+1)
    next_prev_blog.append(prev)
    next_prev_blog.append(_next)
    
    rand_id = random.sample(range(1, tag_id + 1), 6)
    for i in range(5):
        tag = tags.query.get(rand_id[i])
        tag_list.append(tag)

    blog = articles.query.get(id)

    return render_template('single-blog.html', title = blog.title, content = blog.content, cover = blog.cover_photo, popular_tag = tag_list,  recent_blog = blog_list, prev_next = next_prev_blog)
  
@app.route('/login', methods = ['GET', 'POST']) #all about login
def Login():
    form = LoginForm()


    if request.method == 'POST':
        if form.validate_on_submit():
            user = userInfo.query.filter_by(username = form.username.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)

                    return redirect(url_for('home'))

                flash("Invalid Credentials")

        

    return render_template('login.html', title = 'Login', form = form)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        name = form.name.data
        surname = form.surname.data
        username = form.username.data
        password = hashed_password
        email = form.email.data
        phone = form.phone.data
        

        new_register = userInfo(name = name, surname = surname, username = username, password = password, email = email, phone = phone )

        try:
            db.session.add(new_register)
            db.session.commit()
            flash("Registration was successfull!")
        except:
            flash("Unique Credentials (Username, Mail or Phone Number) has already exist! Try to Log In!")

        return redirect(url_for('Login'))

    return render_template('registration.html', form = form)



@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = '%{0}%'.format(search_value)
        results = articles.query.filter(or_(articles.title.like(search), articles.content.like(search))).all()

        return render_template('search_result.html', search_result = results)

    else:
        return redirect('/')


if __name__ =='__main__':  
    app.run(debug = True)  