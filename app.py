from flask import *
from hashlib import sha256
import database, uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']


		
		return redirect(url_for('trips'))

	return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
	return 'NOT IMPLEMENTED'

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		salt = uuid.uuid4().hex

		hashed_password = sha256((password + salt).encode()).hexdigest()

		database.execute('INSERT INTO users VALUES ("{}", "{}", "{}")'.format(username, hashed_password, salt))
		return render_template('register.html', success='User registered successfully')
	return render_template('register.html')

@app.route('/trips', methods=['GET', 'POST'])
def trips():
	if request.method == 'POST':
		id = uuid.uuid4()
		username = request.form['username']
		origin = request.form['origin']
		destination = request.form['destination']

		database.execute('INSERT INTO trips VALUES ("{}", "{}", "{}", "{}")'.format(id, username, origin, destination))
		return render_template('trip_list', success='Trip planned successfully')

	return render_template('trip_list.html')

@app.route('/trips/new', methods=['GET'])
def trip():
	return render_template('trip_form.html')
