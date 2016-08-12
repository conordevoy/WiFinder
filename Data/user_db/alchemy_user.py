from app import db

class User(db.Model):
	__tablename__ = "USER"

	userID = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	permissions = db.Column(db.String, nullable=False)

	def __init__(self, name, email, password, permissions):
		self.name = name
		self.email = email
		self.password = password
		self.permissions = permissions

	def __repr__(self):
		return '<User {} {}'.format(self.userID, self.name)