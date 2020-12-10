from datetime import datetime
from flaskapp import db
from flask_login import UserMixin

words_categories = db.Table('words_categories',
	db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
	db.Column('word_id', db.Integer, db.ForeignKey('words.id'), primary_key=True)
	)

words_users = db.Table('words_users',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
	db.Column('word_id', db.Integer, db.ForeignKey('words.id'), primary_key=True),
	db.Column('is_known', db.Boolean, default=False)
	)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    category_color = db.Column(db.String(25), nullable=False)
    category_description = db.Column(db.String(1000))
    # words = db.relationship('Words', secondary=words_categories, backref='cat_words')
    words = db.relationship('Words', secondary=words_categories, backref=db.backref('words_cat', lazy='select'))

    def __repr__(self):
    	return f"Category: {self.category_name}, {self.category_color}"


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    words = db.relationship('Words', backref='creator', lazy=True)
    unique_words = db.relationship('Words', secondary=words_users, backref=db.backref('uni_user', lazy='select'))

    def __repr__(self):
    	return f"User: {self.username}, {self.email}"

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_name = db.Column(db.String(25), unique=True, nullable=False)
    hebrew_trans = db.Column(db.String(25), nullable=False)
    english_trans = db.Column(db.String(45))
    image_path = db.Column(db.String(5000))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    unique_words = db.relationship('Users', secondary=words_users, backref=db.backref('uni_word', lazy='select'))
    # words = db.relationship('Categories', secondary=words_categories, backref='cats_word')
    words = db.relationship('Categories', secondary=words_categories, backref=db.backref('cats_word', lazy='select'))
    

    def __repr__(self):
    	return f"Word: {self.word_name}, {self.hebrew_trans}, {self.english_trans}, {self.date_created}"
