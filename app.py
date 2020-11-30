from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKey
from sqlalchemy import insert, or_
import time, math, os, random, string
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from flask_login import AnonymousUserMixin
from form import RegisterForm, LoginForm, BlogForm, PassChange
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from multiprocessing import Value


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'img'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


ckeditor = CKEditor(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login' #?

counter = Value('i', 0)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    writer_id = db.Column(db.Integer, db.ForeignKey('userInfo.id'))
    read_time = db.Column(db.Integer)

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    active = db.Column(db.Boolean, default=True, nullable=False)

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


login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    return userInfo.query.get(user_id)

@app.context_processor #to send variable to base.html
def inject_user():
    name = current_user.username
    nname = current_user.name
    admin = current_user.is_admin
    profile_pic = current_user.profile_pic
    
    return dict(name = name, nname = nname, admin = admin, pp = profile_pic, id = current_user.get_id())


@app.route('/')   
def home():

    last_item = articles.query.order_by(articles.id.desc()).first()
    id =  last_item.id
    blog_list = list()
    top_blog_list = list()
    writer = list()
    tb_writer = list()

    for x in range(4):
        top_blog = articles.query.get(id)
        top_blog_list.append(top_blog)
        
        tb_writer_obj = userInfo.query.get(top_blog.writer_id)
        tb_writer.append(tb_writer_obj)


        id = id - 1

    for x in range(6):
        blog = articles.query.get(id)
        blog_list.append(blog)

        writer_obj = userInfo.query.get(blog.writer_id)
        writer.append(writer_obj)

        id = id - 1


    return render_template("index.html", top_blog = zip(top_blog_list, tb_writer), recent_blog = zip(blog_list, writer))


@app.route('/search', methods = ['GET', 'POST'])
def search():

    writer = list()

    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = '%{0}%'.format(search_value)
        results = articles.query.filter(or_(articles.title.like(search), articles.content.like(search))).all()

        for x in results:
            writer_obj = userInfo.query.get(x.writer_id)
            writer.append(writer_obj)

        return render_template('search_result.html', search_result = zip(results, writer))

    else:
        return redirect('/')

@app.route('/all_posts')
def all_posts():
    last_item = articles.query.order_by(articles.id.desc()).first()
    id =  last_item.id
    data = {}

    for x in range(6):

        tempData = []
        tempData.append(articles.query.get(id))
        tempData.append(userInfo.query.get(articles.query.get(id).writer_id))

        data[id] = tempData
        id = id - 1

    print(data)
    return render_template('all_blogs.html', all_blogs = data)

@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.form.get("last_blog_id"):
        id =  int(request.form.get("last_blog_id")) - 1

        data = {}
        for x in range(6):
            if (id == 0):
                break

            tempArticle = articles.query.get(id)
            tempData =  []
            tempData.append(tempArticle.title)
            tempData.append(tempArticle.content)
            tempData.append(tempArticle.cover_photo)
            tempData.append(userInfo.query.get(int(tempArticle.writer_id)).name)
            tempData.append(userInfo.query.get(int(tempArticle.writer_id)).surname)
            tempData.append(tempArticle.date_created.strftime('%d-%m-%Y'))

            data[id] = tempData
            id = id - 1             
            res = data
        else:
            res = data
        
    return res


@app.route('/blog/<int:id>')
def blog(id):

    with counter.get_lock():
        counter.value += 1
        out = counter.value
    
    
    blog = articles.query.get(id)

    blog.view = out
    db.session.commit()

    writer_obj = userInfo.query.get(blog.writer_id)

    last_item = articles.query.order_by(articles.id.desc()).first()
    last_blog_id =  last_item.id
    blog_list = list()
    rw = list()

    rand_id = random.sample(range(1, last_blog_id + 1), 3)
    for i in range(3):
        post = articles.query.get(rand_id[i])
        blog_list.append(post)

        related_writer = userInfo.query.get(post.writer_id)
        rw.append(related_writer)

    return render_template('post.html', post = blog, writer = writer_obj, related_post = zip(blog_list, rw), view = blog.view)

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

        

    return render_template('login.html', form = form)

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
  
    return render_template('register.html', form = form)



@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))

@app.route('/blog_write', methods = ['GET', 'POST'])
@login_required
def blog_write():
    form = BlogForm()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        res = len(content.split())

        count = round(res / 200)

        file = request.files['photo']

        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)
        
        if allowed_file(file.filename):
            filename = get_random_string(8) + secure_filename(file.filename)
            file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
            photo = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace(os.sep, '/')
        else:
            flash("Non allowed file format")
            return redirect(request.url)

        new_blog = articles(title = title, content = content, cover_photo = photo, likes = 12, view = 1, writer_id = current_user.get_id(), read_time = count)

        try:
            db.session.add(new_blog)
            db.session.commit()
            flash("Blog added successfully!")
        except:
            flash("Full all fields")

        return redirect(url_for('home'))

    return render_template('blog_write.html', form = form)

@app.route('/pass_change', methods = ['GET', 'POST'])
@login_required
def pass_change():
    form = PassChange()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        
        password = hashed_password
        
        current_user.password = password

        try:
            db.session.commit()
            flash("Password changed successfully!")
            logout_user()
        except:
            flash("Passwords do not match!")

        return redirect(url_for('Login'))

    return render_template('pass_change.html', form = form)

@app.route('/add_pp', methods = ['GET', 'POST'])
@login_required

def add_pp():
    if request.method == 'POST':
        file = request.files['photo']

        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)
        
        if allowed_file(file.filename):
            filename = get_random_string(8) + secure_filename(file.filename)
            file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
            photo = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace(os.sep, '/')
        else:
            flash("Non allowed file format")
            return redirect(request.url)

        obj = userInfo.query.get(current_user.get_id())
        obj.profile_pic = photo
        db.session.commit()
            
        flash("Blog added successfully!")
        return redirect(url_for('home'))

    return render_template('pp_change.html')

@app.route('/authors')
def authors():
    
    temp = userInfo.query.with_entities(userInfo.id).all()
    temp2 = articles.query.with_entities(articles.writer_id).all()
    writer = list()
    authors = list()

    for x in range(len(temp2)):
        for y in range(len(temp)):
            if temp[y][0] == temp2 [x][0]:
                writer.append(temp[y][0])

    writer = list(set(writer))
    post_bywriter = list()

    for x in writer:
        authors.append(userInfo.query.get(x))

    for y in range(len(writer)):
        count = 0
        for x in range(len(temp2)):
            if writer[y] == temp2[x][0]:
                count += 1
        post_bywriter.append(count)


    print(authors)

    return render_template('authors.html', authors = zip(authors, post_bywriter))

@app.route('/author/<int:id>')
def author(id):

    author = userInfo.query.get(id)
    blogs = articles.query.filter_by(writer_id = id).all()

    print(author)
    print(blogs)



    return render_template('author.html', author = author, blogs = blogs)


if __name__ =='__main__':  
    app.run(debug = True)  