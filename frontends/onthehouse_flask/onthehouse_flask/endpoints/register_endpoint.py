import flask; from flask import render_template, flash, request
from flask_login import current_user, login_user
import wtforms
from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
import recipedb
#from Objects import User


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
        #common.add(user)
        #db.session.commit()
        #need connection to db
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    displayname = StringField('Displayname', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

