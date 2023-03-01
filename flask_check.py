# pip install flask_sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
# create a new user
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()

# retrieve all users
users = User.query.all()

# retrieve a single user by id
user = User.query.get(1)

# filter by a single condition
users = User.query.filter(User.username == 'john').all()

# filter by multiple conditions
users = User.query.filter((User.username == 'john') | (User.email == 'john@example.com')).all()

# filter using comparison operators
users = User.query.filter(User.id > 10).all()

# filter using string methods
users = User.query.filter(User.username.startswith('j')).all()

# filter using a subquery
subquery = db.session.query(User.id).filter(User.username == 'john')
users = User.query.filter(User.id.in_(subquery)).all()
