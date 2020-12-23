from flask import *
from flask_sqlalchemy import SQLAlchemy
import random, string
from flask_ckeditor import CKEditor
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


ckeditor = CKEditor(app)

db = SQLAlchemy(app)


#some global functions
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from myapp import views