# from flaskapp import app
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FieldList
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import Users

class LoginForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
	# submit = SubmitField('Log_In')


class RegistrationForm(FlaskForm):
	email = StringField('email',validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)])
	username = StringField('username',validators=[InputRequired(), Length(min=4, max=30)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	# submit = SubmitField('Sign_Up')

	def validate_username(self, username):
		user = Users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')


class UpdateAccountForm(FlaskForm):
	email = StringField('email',validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)])
	username = StringField('username',validators=[InputRequired(), Length(min=4, max=30)])
	# submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = Users.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.') 

class CardForm(FlaskForm):
	name = StringField('Word Name', validators=[DataRequired()])
	heb_trans = StringField('Word in Hebrew', validators=[DataRequired()])
	eng_trans = StringField('Word in English', validators=[DataRequired()])
	category = StringField('Word Category', validators=[DataRequired()])

	def validate_word(self, name):
		word = Words.query.filter_by(word_name=name.data).first()
		if word:
			raise ValidationError('This word was already created.')

class CategoryForm(FlaskForm):
	name = StringField('Category Name', validators=[DataRequired()])
	color = StringField('Category color (in HEX)', validators=[DataRequired()])
	exp = TextAreaField('Category Description', validators=[DataRequired()])

	def validate_category(self, name):
		category = Categories.query.filter_by(category_name=name.data).first()
		if category:
			raise ValidationError('This category was already created.')