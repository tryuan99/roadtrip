from flask import *
import database, uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/trips', methods=['GET', 'POST'])
def trips():
	if request.method == 'POST':
		id = uuid.uuid4()
		username = request.form['username']
		origin = request.form['origin']
		destination = request.form['destination']

		database.execute('INSERT INTO trips VALUES ({}, {}, {}, {})'.format(id, username, origin, destination))
		return render_template('trip_list.html')
	
	return render_template('trip_list.html')

@app.route('/trips/new', methods=['GET'])
def trip():
	return render_template('trip_form.html')
