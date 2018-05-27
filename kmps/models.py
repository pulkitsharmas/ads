from dbsetup import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(20), nullable=False)
	type = db.Column(db.Integer, nullable=False)
	profile_filename = db.Column(db.String(80), nullable=False)
	profile_url = db.Column(db.String(80), nullable=False)
	department_id = db.Column(db.Integer, db.ForeignKey('department.did'))
	department = db.relationship('Department')
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.oid'))
	organization = db.relationship('Organization')

class Organization(db.Model):
	oid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

class Department(db.Model):
	did = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(200), nullable=False)
	isfin = db.Column(db.Boolean, nullable=False)
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.oid'))
	organization = db.relationship('Organization')

class Brequest(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(180), nullable=False)
	ammount = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	man_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	fman_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', foreign_keys = 'Brequest.user_id')
	man = db.relationship('User', foreign_keys = 'Brequest.man_id')
	fman = db.relationship('User', foreign_keys = 'Brequest.fman_id')

class Rejects(db.Model):
	rj_id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.String(80), nullable=False)
	brequest_id = db.Column(db.Integer, db.ForeignKey('brequest.rid'))
	brequest = db.relationship('Brequest')

class Docq(db.Model):
	doc_id = db.Column(db.Integer, primary_key=True)
	caption = db.Column(db.String(80), nullable=False)
	filename = db.Column(db.String(80), nullable=False)
	doc_url = db.Column(db.String(80), nullable=False)
	brequest_id = db.Column(db.Integer, db.ForeignKey('brequest.rid'))
	brequest = db.relationship('Brequest')