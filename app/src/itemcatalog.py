import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    DATABASE=os.path.join(app.root_path, 'itemcatalog.db'),
    SECRET_KEY=b'6\x10m|\xa6iK\xf2Sv\r\xf9\x0e\x13\xfe\xcd',
    USERNAME='admin',
    PASSWORD='default'
)


def connect_db():
    '''Connects to the specific database.'''
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    '''Opens a new database connection if there is none yet for the
    current application context.
    '''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request.'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    '''Initializes the database.'''
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_items():
    db = get_db()
    cur = db.execute('select title, description from items order by id desc')
    items = cur.fetchall()
    return render_template('show_items.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into items (title, description) values (?, ?)',
               [request.form['title'], request.form['description']])
    db.commit()
    flash('New item was successfully posted')
    return redirect(url_for('show_items'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_items'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_items'))
