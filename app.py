from flask import *
from hashlib import sha256
import config
import database
import uuid

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        record = database.fetchone('SELECT password, salt FROM users WHERE username="{}";'.format(username))
        if not record:
            return render_template('login.html', error='Invalid username or password')

        correct_password, salt = record
        hashed_password = sha256((password + salt).encode()).hexdigest()

        if hashed_password != correct_password:
            return render_template('login.html', error='Invalid username or password')

        session['username'] = username
        return redirect(url_for('trips'))

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        salt = uuid.uuid4().hex

        hashed_password = sha256((password + salt).encode()).hexdigest()

        database.execute('INSERT INTO users VALUES ("{}", "{}", "{}");'.format(username, hashed_password, salt))
        return render_template('register.html', success='User registered successfully')
    return render_template('register.html')


@app.route('/trips', methods=['GET', 'POST'])
def trips():
    if request.method == 'POST':
        id = uuid.uuid4()
        username = request.form['username']
        origin = request.form['origin']
        destination = request.form['destination']

        database.execute('INSERT INTO trips VALUES ("{}", "{}", "{}", "{}");'.format(id, username, origin, destination))
        return render_template('trip_list', success='Trip planned successfully')

    return render_template('trip_list.html')


@app.route('/trips/new', methods=['GET', 'POST'])
def trip():
    if request.method == 'POST':
        id = uuid.uuid4()
        origin = request.form['origin']
        destination = request.form['destination']
        seats = request.form['seats']
        username = session['username']

        database.execute('INSERT INTO trips VALUES ("{}", "{}", "{}", "{}", "{}");'.format(id, username, origin, destination, seats))
    return render_template('trip_form.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('error.html', message=error), 500
