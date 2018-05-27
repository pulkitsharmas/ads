from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo, Email, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

from models import User, Organization, Department


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired()])
	submit = SubmitField('Login')

class RegisterAdmin(FlaskForm):
	oname = StringField('Organization Name', validators=[InputRequired()])
	name = StringField('Administrator Name', validators=[InputRequired()])
	email = StringField('Email', validators=[InputRequired(),Email()])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=12)])
	confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_oname(self, oname):
		org = Organization.query.filter_by(name=oname.data).first()
		if org is not None:
			raise ValidationError('Organization already registered.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already registered.')

class DepartmentNewEdit(FlaskForm):
	name = StringField('Department Name', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	isfin = BooleanField('Finance Department')
	submit = SubmitField('Submit')

	def validate_name(self, name):
		d = Department.query.filter_by(name=name.data).first()
		if d is not None:
			raise ValidationError('Department Name already registered.')

class DeleteForm(FlaskForm):
	submit = SubmitField("Delete")

class UserAdd(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	email = StringField('Email', validators=[InputRequired(),Email()])
	type = SelectField('Type', coerce=int,choices=[(3,'Regular'),(2,'Manager'),(1,'Administrator')])
	dept_id = SelectField('Department', coerce=int)
	submit = SubmitField('Submit')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already registered.')

class RequestAdd(FlaskForm):
	title = StringField('Title', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	ammount = IntegerField('Ammount', validators=[NumberRange(min=0,max=1000000,message="0-1000000")])
	man = SelectField('Manager', coerce=int)
	fman = SelectField('Finance Manager',coerce=int)
	submit = SubmitField('Submit')

class UploadForm(FlaskForm):
	upload = FileField('Media', validators=[FileRequired()])
	submit = SubmitField('Upload')

class OptUploadForm(FlaskForm):
	upload = FileField('Media')
	submit = SubmitField('Upload')

class ARForm(FlaskForm):
	comment = StringField('Comments', validators=[InputRequired()])
	submit = SubmitField('Submit')

class EditProfile(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	email = StringField('Email', validators=[Email(),InputRequired()])
	submit = SubmitField('Submit')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already registered.')

class ChangePass(FlaskForm):
	old = PasswordField('Old Password', validators=[InputRequired()])
	new = PasswordField('New Password', validators=[InputRequired(), Length(min=6,max=12)])
	confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new')])
	submit = SubmitField('Submit')

