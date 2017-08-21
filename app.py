from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template, session, flash
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:134679@localhost/test_accounts'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True


app.debug = True
db = SQLAlchemy(app)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    birth_date = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, name, country, birth_date, email, password):
        self.name = name
        self.country = country
        self.birth_date = birth_date
        self.email = email
        self.password = password


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('sign_in'))
    return wrap

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    return render_template('sign_in.html')

@app.route('/home')
@login_required
def home():
    if 'id' in session:
        user = User.query.filter_by(id = session['id']).first()
        return render_template('user_home.html',
                                name = user.name, email = user.email,
                                country= user.country, birth_day = user.birth_date)
    else:
        return render_template('sign_in.html')

@app.route('/post_user', methods=['POST'])
def post_user():
    if(request.form['password'] == request.form['confirm_password']):
        user = User(request.form['name'], request.form['country'],
                    request.form['birth_date'], request.form['email_address'],
                    request.form['password'])
        test_email = User.query.filter_by(email = user.email).first()
        if( test_email == None):
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('sign_in'))
        else:
            return render_template('sign_up.html',
                                    error=True,
                                    error_message = "Error, This email exists.")

    else:
        return render_template('sign_up.html',
                                error=True,
                                error_message = "Error, password mismatch")

@app.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    input_data = {'email':request.form['email_address'],
                  'password':request.form['password']}
    correct_data = User.query.filter_by(email = input_data['email']).first()

    if(correct_data == None):
        return render_template('sign_in.html',
               error=True, error_message="account not found!!")

    if (correct_data.password == input_data['password']):
        session['logged_in'] = True
        session['id'] = correct_data.id
        return redirect(url_for('home'))
    else:
        return render_template('sign_in.html', error=True, error_message='Wrong password!!')




if(__name__ == "__main__"):
    app.run()
