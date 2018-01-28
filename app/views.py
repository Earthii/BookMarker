from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db, login_manager
from app.forms import BookmarkForm, LoginForm, SignupForm
from app.models import User, Bookmark

# Flask login needs to access user instances
# tells the login manager how to retrieve user objects based in the id
# when logged in, the id is stored in the http Session
# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


# app.url_map shows all the routes which maps to functions
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)  # flask login sets cookies if they want to be remembered
            flash("Logged in successfully as {}".format(user.username))
            # the next, is to redirect to the old url that a user might have tried to access with permission prior to login
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    username = current_user.username
    logout_user()
    flash('{} has successfully logged out!'.format(username))
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email= form.email.data,
                    username= form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}!'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/")
@app.route("/index")
def index():
    # render_template will look in templates folder by default
    return render_template("index.html", new_bookmarks=Bookmark.newest(5))


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)  # fill form with the data from the database
    if form.validate_on_submit():
        form.populate_obj(bookmark)  # copy form data into bookmark
        db.session.commit()            # bookmark object is already in the session since we made a get
        flash('Stored "{}"'.format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title= "Edit bookmark")

# Accept both methods
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # if get, form is empty, but if post, form has data
    form = BookmarkForm()
    # if request.method == "POST":
    if form.validate_on_submit():
        # url = request.form['url']
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash('Stored {0}'.format(description))
        return redirect(url_for('index'))
    return render_template("add.html", form=form)


# parameter in url passed into function
@app.route('/user/<username>')
def user(username):
    # if not found, it will throw 404
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


# Returning error pages, important to return a tuple with the error code
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 400


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # debug mode
    # app.run(debug=True)
    app.run()