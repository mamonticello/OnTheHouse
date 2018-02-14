import flask; from flask import render_template, flash, request
from Objects import User
from . import forms 
from forms import RegistrationForm
from flask_login import current_user, login_user

from . import common

site = common.site

@site.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_displayname(form.displayname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@site.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@site.route('/secret')
def secret():
    return "You have successfully logged in"

if __name__ == '__main__':
    app.run(debug=True)

        def check_password(hashed_password, user_password):
        return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

    def validate(username, password):
        con = sqlite3.connect('static/user.db')
        completion = False
        with con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Users")
                    rows = cur.fetchall()
                    for row in rows:
                        dbUser = row[0]
                        dbPass = row[1]
                        if dbUser==username:
                            completion=check_password(dbPass, password)
        return completion