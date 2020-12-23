from flask import *
from sqlalchemy import or_
import random
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, BlogForm, PassChange
from werkzeug.utils import secure_filename
from multiprocessing import Value

from .__init__ import app
from myapp.models import *


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login' #?

    
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
    
    count = 4

    for x in range(50):
        if count != 0:
            top_blog = articles.query.get(id)
        
            if top_blog.active == True:
                top_blog_list.append(top_blog)
                tb_writer_obj = userInfo.query.get(top_blog.writer_id)
                tb_writer.append(tb_writer_obj)
                count = count - 1
            
        else:
            break

        id = id - 1


    count2 = 6
    for x in range(50):
        if count2 != 0:
            blog = articles.query.get(id)

            if blog.active == True:
                blog_list.append(blog)
                writer_obj = userInfo.query.get(blog.writer_id)
                writer.append(writer_obj)
                count2 = count2 - 1
        
        else:
            break

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
        #.filter_by(articles.active == True)

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
    

    count = 6
    for x in range(50):
        if count != 0:
            article = articles.query.get(id)

            if article.active == True:
                tempData = []
                tempData.append(articles.query.get(id))
                tempData.append(userInfo.query.get(articles.query.get(id).writer_id))
                count = count - 1
            
                
                data[id] = tempData
            id = id - 1
        else:
            break

    return render_template('all_blogs.html', all_blogs = data)

@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.form.get("last_blog_id"):
        id =  int(request.form.get("last_blog_id")) - 1

        data = {}
        count = 6
        for x in range(50):
            if (id == 0):
                break

            if count != 0:
                tempArticle = articles.query.get(id)

                if tempArticle.active == True:
                    tempData =  []
                    tempData.append(tempArticle.title)
                    tempData.append(tempArticle.content)
                    tempData.append(tempArticle.cover_photo)
                    tempData.append(userInfo.query.get(int(tempArticle.writer_id)).name)
                    tempData.append(userInfo.query.get(int(tempArticle.writer_id)).surname)
                    tempData.append(tempArticle.date_created.strftime('%d-%m-%Y'))
                    count = count - 1
                    data[id] = tempData
            else:
                break

            id = id - 1             
            res = data
        if id != 0:
            res = data
        
    return res

counter = Value('i', 0)
@app.route('/blog/<int:id>')
def blog(id):
    blog = articles.query.get(id)

    counter.value = blog.view

    with counter.get_lock():
        counter.value += 1
        out = counter.value
    

    blog.view = out
    db.session.commit()

    writer_obj = userInfo.query.get(blog.writer_id)

    last_item = articles.query.order_by(articles.id.desc()).first()
    last_blog_id =  last_item.id
    blog_list = list()
    rw = list()

    rand_id = random.sample(range(1, last_blog_id + 1), last_blog_id)

    count = 3
    for i in range(50):
        if count != 0:
            post = articles.query.get(rand_id[i])
            if post.active == True:
                blog_list.append(post)

                related_writer = userInfo.query.get(post.writer_id)
                rw.append(related_writer)
                count = count - 1
            else:
                return ('Blog not is avaible or in hold!')
        
        else:
            break

    return render_template('post.html', post = blog, writer = writer_obj, related_post = zip(blog_list, rw), view = blog.view)

@app.route('/login', methods = ['GET', 'POST']) #all about login
def Login():
    form = LoginForm()


    if request.method == 'POST':
        if form.validate_on_submit():
            user = userInfo.query.filter_by(username = form.username.data).first()

            if user:
                if user.active == True:
                    if check_password_hash(user.password, form.password.data):
                        login_user(user)

                        return redirect(url_for('home'))

                    flash("Invalid Credentials")

            else:
                flash("Your account is currently in hold. Please contact with admin.")

        

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
    
    real_temp2 = list()
    temp = userInfo.query.with_entities(userInfo.id).all()
    temp2 = articles.query.with_entities(articles.writer_id).all()
    blogs = articles.query.all()

    for x in range(len(temp2)):
        if blogs[x].active == True:
            real_temp2.append(blogs[x].writer_id)
    
    writer = list()
    authors = list()

    for x in range(len(real_temp2)):
        for y in range(len(temp)):
            if temp[y][0] == real_temp2[x]:
                writer.append(temp[y][0])

    writer = list(set(writer))
    post_bywriter = list()

    for x in writer:
        authors.append(userInfo.query.get(x))
    
    print(temp2)

    for y in range(len(writer)):
        count = 0
        for x in range(len(temp2)):
            if writer[y] == blogs[x].writer_id:
                if blogs[x].active == True:
                    count += 1
        
        post_bywriter.append(count)

    return render_template('authors.html', authors = zip(authors, post_bywriter))

@app.route('/author/<int:id>')
def author(id):
    blog = list()

    author = userInfo.query.get(id)
    blogs = articles.query.filter_by(writer_id = id).all()

    for x in range(len(blogs)):
        if blogs[x].active == True:
            blog.append(blogs[x])


    return render_template('author.html', author = author, blogs = blog)

@app.route('/admin/user')
@login_required
def admin_user():

    users = userInfo.query.all()

    if current_user.is_admin == 1:
        return render_template('admin-user.html', users = users)
    else:
        return "Access Denied!"

@app.route('/admin/blog')
@login_required
def admin_blog():

    blogs = articles.query.all()
    authors = list()

    for x in range(len(blogs)):
        authors.append(userInfo.query.get(blogs[x].writer_id))

    if current_user.is_admin == 1:
        return render_template('admin-blog.html',db = zip(blogs, authors))
    else:
        return "Access Denied!"

@app.route('/deactivate/<int:id>')
def deactivate(id):
    blog = articles.query.filter_by(id = id).first()

    blog.active = False
    db.session.commit()

    return redirect('/admin/blog')

@app.route('/activate/<int:id>')
def activate(id):
    blog = articles.query.filter_by(id = id).first()

    blog.active = True
    db.session.commit()

    return redirect('/admin/blog')

@app.route('/ban/<int:id>')
def ban(id):
    user = userInfo.query.filter_by(id = id).first()

    user.active = False
    db.session.commit()

    return redirect('/admin/user')

@app.route('/unban/<int:id>')
def unban(id):
    user = userInfo.query.filter_by(id = id).first()

    user.active = True
    db.session.commit()

    return redirect('/admin/user')
