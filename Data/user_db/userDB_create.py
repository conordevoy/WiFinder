from app import db
from alchemy_user import User

db.create_all()

db.session.add(User('admin', 'admin@ucd.ie', 'wifinder', 'A'))
db.session.add(User('user', 'user@ucd.ie', 'password', 'U'))

db.session.commit()