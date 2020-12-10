from flask import render_template, request, url_for, redirect, flash, abort
from flaskapp import app, db, login_manager
from flask_wtf.file import FileField, FileAllowed
from flaskapp.models import Words, Users, Categories, words_users, words_categories
from flaskapp.forms import LoginForm, RegistrationForm, UpdateAccountForm, CardForm, CategoryForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


@app.route('/', methods=['POST', 'GET'])
def index():
	if current_user.is_authenticated:
   		return render_template("index.html", name=current_user.username)
	else:
		return render_template("index.html", title='Home')

@app.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		for word in Words.query.all():
			word.uni_user.append(new_user)
		db.session.commit()
		flash(f'Account has been created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				next_page = request.args.get('next')
				if next_page:
					return redirect(next_page)
				return redirect(url_for('index', username=current_user.username))
		flash('Invalid username or password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Login', form=form)

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET': # not to re-sent data
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form=form, name=current_user.username)

@app.route("/card/new", methods=['POST', 'GET'])
@login_required
def new_card():
	form = CardForm()
	if form.validate_on_submit():
		new_word = Words(creator=current_user, word_name=form.name.data, hebrew_trans=form.heb_trans.data, english_trans=form.eng_trans.data)
		db.session.add(new_word)
		db.session.commit()
		for user in Users.query.all():
			# new_word.uni_user.append(user)
			new_word.uni_user.append(user)
		db.session.commit()
		cat = Categories.query.filter_by(category_name=form.category.data).first()
		new_word.words_cat.append(cat)
		db.session.commit()
		flash('Your card has been created!', 'success')
		return redirect(url_for('words'))
	return render_template('new_word.html', title='New Word', form=form, legend='Create a new word', name=current_user.username)

@app.route("/category/new", methods=['POST', 'GET'])
@login_required
def new_category():
	form = CategoryForm()
	if form.validate_on_submit():
		category = Categories(category_name=form.name.data, category_color=form.color.data, category_description=form.exp.data)
		db.session.add(category)
		db.session.commit()
		cats = Categories.query.all()
		flash('New category has been created!', 'success')
		return redirect(url_for('categories', cats=cats))
	cats = Categories.query.all()
	return render_template('new_category.html', title='New Category', form=form, legend='Create a new word', name=current_user.username, cats=cats)

@app.route('/categories', methods=['POST', 'GET'])
@login_required
def categories():
	cats = Categories.query.all()
	return render_template("categories.html", title='Categories', cats=cats, name=current_user.username)

@app.route('/my_words', methods=['POST', 'GET'])
@login_required
def words():
	words = Words.query.all()
	return render_template("words.html", title='Words', words=words, name=current_user.username)

@app.route('/card/<int:card_id>')
@login_required
def card(card_id):
	card = Words.query.get_or_404(card_id)
	return render_template("card.html", title='Card', card=card, name=current_user.username)

@app.route('/card/<int:card_id>/update', methods=['POST', 'GET'])
@login_required
def update_card(card_id):
	card = Words.query.get_or_404(card_id)
	form = CardForm()
	if form.validate_on_submit():
		card.word_name = form.name.data
		card.hebrew_trans = form.heb_trans.data
		card.english_trans = form.eng_trans.data
		db.session.commit()
		flash('Your word has been updated!', 'success')
		return redirect(url_for('card', card_id=card.id))
	elif request.method == 'GET':
		form.name.data = card.word_name
		form.heb_trans.data = card.hebrew_trans
		form.eng_trans.data = card.english_trans 
	# form.category.data = card.category 
	return render_template("new_word.html", title='Update Card', card=card, form=form, name=current_user.username, legend='Update word')

@app.route('/card/<int:card_id>/delete', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_card(card_id):
	card = Words.query.get_or_404(card_id)
	try:
		db.session.delete(card)
		db.session.commit()
		flash('Your word has been deleted', 'success')
		return redirect(url_for('words'))
	except Exception as e:
		return f"There was an error deleting: {e}"


# @app.route('/learn_words', methods=['POST', 'GET'])
# @login_required
# def learn_words():
# 	# words = db.session.query(current_user.uni_word).filter(current_user.uni_word.is_known == False).all()
# 	words = current_user.query.filter(current_user.is_known == False).all()
# 	return render_template("learn_words.html", title='Learn Card', words=words, name=current_user.username)

# def unknown_words():
# 	user = Users.query.get(user_id='1')
# 	words = user.uni_word.query.filter(current_user.uni_word.is_known == False).all()
# 	for w in words:
# 		print(current_user.uni_word.name)