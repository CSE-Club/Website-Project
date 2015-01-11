from flask import Blueprint, render_template, redirect, url_for

from util.auth import Auth
from util.session import Session, loggedin
from forms.login import LoginForm

# Used simply for creating a test user, remove it when project is complete
from loader import bcrypt, db
from models.user import User
from datetime import datetime

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
@blueprint.route('/index')
def index():
    form = LoginForm()

    return render_template('login.html', form=form)


@blueprint.route('/login', methods=["POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if Auth.check(form.username.data, form.password.data):
            Auth.login(form.username.data, form.password.data)

            return 'Logged in! :)'

    return 'Not logged in :('


@blueprint.route('/loggedin')
@loggedin
def loggedinpage():
    return 'Still logged in! <a href="/logout">Sign out</a>'


@blueprint.route('/logout')
def logout():
    Session.destroy()

    return redirect(url_for('.index'))

# This can be treated as an example of how to create a user/how to add something to the database. However, we aren't
# going to be using this particular function other than for testing purposes
@blueprint.route('/mktestuser')
def mktestuser():

    user = User()
    user.username = "test"
    user.password = bcrypt.generate_password_hash("test")
    user.email = 'test@example.com'
    user.created = datetime.now()
    user.role = 0

    db.session.add(user)
    db.session.commit()

    return "Done. username=\"test\", password=\"test\""