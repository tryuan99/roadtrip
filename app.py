from flask import *
from functools import wraps
from hashlib import sha256

import config
import database
import uuid
import requests

app = Flask(__name__)
app.config.from_object('config')

def login_required(f):
    @wraps(f)
    def with_login(*args, **kwargs):
        if session.get('username', None) is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return with_login


def get_trip_obj(record):
    keys = [
        'id', 'username', 'origin', 'originLat', 'originLng',
        'destination', 'destinationLat', 'destinationLng',
        'seats', 'fare', 'date', 'time'
    ]
    return dict(zip(keys, record))


@app.route('/', methods=['GET'])
def index():
    if session.get('username', None) is not None:
        return redirect(url_for('trips'))

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

    if session.get('username', None) is not None:
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
@app.route('/trips/<radius><originLat><originLng><destinationLat><destinationLng>', methods=[])
@login_required
def trips():

    if request.method == 'POST':
        id = uuid.uuid4()
        username = session['username']
        origin = request.form['origin']
        originLat = request.form['originLat']
        originLng = request.form['originLng']
        destination = request.form['destination']
        destinationLat = request.form['destinationLat']
        destinationLng = request.form['destinationLng']
        seats = request.form['seats']
        fare = request.form['fare']
        date = request.form['date']
        time = request.form['time']

        database.execute(
            'INSERT INTO trips VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
                id, username, origin, originLat, originLng, destination, destinationLat, destinationLng, seats, fare, date, time
            )
        )
        return redirect(url_for('trip', id=id))


    radius = request.args.get('radius', None)
    originLat = request.args.get('originLat', None)
    originLng = request.args.get('originLng', None)
    destinationLat = request.args.get('destinationLat', None)
    destinationLng = request.args.get('destinationLng', None)


    all_trips = database.fetchall('SELECT * FROM trips WHERE DATE >= date("now");')
    trips = list(map(get_trip_obj, all_trips))
    return render_template('trip_list.html', trips=trips)


@app.route('/trips/new', methods=['GET'])
@login_required
def new_trip():
    return render_template('trip_form.html')


@app.route('/trips/<uuid:id>', methods=['GET', 'POST'])
@login_required
def trip(id=None):
    trip = database.fetchone('SELECT * FROM trips WHERE id="{}"'.format(id))
    if not trip:
        return render_template('trips.html', error='Invalid trip ID')
    trip = get_trip_obj(trip)

    if request.method == 'POST':
        username = session['username']

        database.execute('INSERT INTO carpools VALUES ("{}", "{}")'.format(id, username))
        return render_template('trip.html', trip=trip, success='Trip joined successfully')

    return render_template('trip.html', trip=trip)


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def error(error):
    return render_template('error.html', message=error), 500
