from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:134679@localhost/test_accounts'

app.debug = True
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    return render_template('sign_in.html')

@app.route('/index')
def my_index():
    return render_template('index.html')

@app.route('/post_user', methods=['POST'])
def post_user():
    if(request.form['password'] == request.form['confirm_password']):
        user = User(request.form['name'], request.form['country'], request.form['birth_date'], request.form['email_address'], request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('sign_up'))


@app.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    input_data = {'email':request.form['email_address'], 'password':request.form['password']}
    try:
        correct_data = User.query.filter_by(email = input_data['email']).first()
    except:
        print("account not found!!")
        return redirect(url_for('sign_in'))

    if (correct_data.password == input_data['password']):
        return redirect(url_for('index'))
    else:
        print('Wrong password!!')
        return redirect(url_for('sign_in'))


if(__name__ == "__main__"):
    app.run()
