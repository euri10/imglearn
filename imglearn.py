from flask import Flask, render_template, request, flash, url_for, redirect
from flask.ext.login import login_user, unicode, LoginManager, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from wtforms import StringField, Form, validators, PasswordField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///botdb.db'
app.secret_key = 'my precious key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.filter(User.id == int(user_id)).first()


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


class LoginForm(Form):
    email = StringField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            flash('You were logged in. Go Crazy.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form, error=error)


class RegisterForm(Form):
    email = StringField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Please repeat password')])
    confirm = PasswordField('Repeat password')


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    else:
        error = 'Please make sure you enter a real email and passwords match'
    return render_template('register.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)
