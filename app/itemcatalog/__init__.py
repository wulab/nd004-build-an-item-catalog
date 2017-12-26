import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from urllib.parse import urlencode


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    CLIENT_ID=os.getenv('OAUTH2_CLIENT_ID'),
    DATABASE=os.path.join(app.root_path, 'itemcatalog.db'),
    SECRET_KEY=b'6\x10m|\xa6iK\xf2Sv\r\xf9\x0e\x13\xfe\xcd'
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


@app.route('/', defaults={'fmt': 'html'})
@app.route('/items', defaults={'fmt': 'html'})
@app.route('/items.<fmt>')
def show_items(fmt):
    db = get_db()
    cur = db.execute('select * from categories order by id')
    categories = cur.fetchall()
    cur = db.execute('select * from items order by id desc')
    items = cur.fetchall()

    if fmt == 'json':
        return jsonify(categories=[dict(c) for c in categories],
                       items=[dict(i) for i in items])

    item = None
    if 'selected' in request.args:
        cur = db.execute('select * from items where id = ?',
                         request.args['selected'])
        item = cur.fetchone()

    return render_template('show_items.html',
                           categories=categories,
                           items=items,
                           item=item)


@app.route('/categories/<category_id>/items', defaults={'fmt': 'html'})
@app.route('/categories/<category_id>/items.<fmt>')
def show_category_items(category_id, fmt):
    db = get_db()
    cur = db.execute('select * from categories order by id')
    categories = cur.fetchall()
    cur = db.execute('''\
        select * from items where items.category_id = ? order by id desc
        ''', category_id)
    items = cur.fetchall()

    if fmt == 'json':
        return jsonify(categories=[dict(c) for c in categories],
                       items=[dict(i) for i in items])

    item = None
    if 'selected' in request.args:
        cur = db.execute('select * from items where id = ?',
                         request.args['selected'])
        item = cur.fetchone()

    return render_template('show_category_items.html',
                           categories=categories,
                           items=items,
                           item=item)


@app.route('/items/new')
def new_item():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select * from categories order by id')
    categories = cur.fetchall()
    cur = db.execute('select * from items order by id desc')
    items = cur.fetchall()
    return render_template('new_item.html',
                           categories=categories,
                           items=items)


@app.route('/items', methods=['POST'])
def create_item():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('''\
        insert into items (title, note, purchase_price, image_url, category_id)
        values (?, ?, ?, ?, ?)
        ''', [
            request.form['title'] or 'Untitled',
            request.form['note'],
            request.form['purchase_price'],
            request.form['image_url'] or 'http://via.placeholder.com/150x200',
            request.form['category_id']
        ])
    db.commit()
    flash('New item was successfully posted')
    return redirect(url_for('show_items'))


@app.route('/items/<item_id>/edit')
def edit_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select * from categories order by id')
    categories = cur.fetchall()
    cur = db.execute('select * from items order by id desc')
    items = cur.fetchall()
    cur = db.execute('select * from items where id = ?', item_id)
    item = cur.fetchone()
    return render_template('edit_item.html',
                           categories=categories,
                           items=items,
                           item=item)


@app.route('/items/<item_id>', methods=['POST'])
def update_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('''\
        update items set
        title = ?, note = ?, purchase_price = ?, image_url = ?, category_id = ?
        where id = ?
        ''', [
            request.form['title'] or 'Untitled',
            request.form['note'],
            request.form['purchase_price'],
            request.form['image_url'] or 'http://via.placeholder.com/150x200',
            request.form['category_id'],
            item_id
        ])
    db.commit()
    flash('Item was successfully updated')
    return redirect(url_for('show_items'))


@app.route('/items/<item_id>/delete', methods=['POST'])
def destroy_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('delete from items where id = ?', item_id)
    db.commit()
    flash('Item was successfully deleted')
    return redirect(url_for('show_items'))


@app.route('/login')
def login():
    params = dict(
        client_id=app.config['CLIENT_ID'],
        redirect_uri=url_for('oauth2callback', _external=True),
        scope='profile',
        response_type='code'
    )
    authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    authorization_url += urlencode(params)
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    if 'code' not in request.args:
        return redirect(url_for('login'))
    else:
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('show_items'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_items'))
