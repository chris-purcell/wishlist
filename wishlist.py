# import all the things
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for,
     abort, render_template, flash)
from contextlib import closing

# create our little wishlist application
app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('instance/config.py')

# Database functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def show_wishlist():
    cur = g.db.execute('select title, text from wishlist order by id desc')
    wishlist = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_wishlist.html', wishlist=wishlist)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into wishlist (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_wishlist'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('show_wishlist'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('show_wishlist'))

if __name__ == '__main__':
    app.run()
