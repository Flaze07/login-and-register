import flask
import json
import firebase_admin as fb
from firebase_admin import firestore

users = {}

app = flask.Flask(__name__)

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def main_page():
	return flask.render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
	if flask.request.method == 'POST':
		username = flask.request.form['username']
		password = flask.request.form['password']
		doc_ref = user_ref.document(username)
		doc = doc_ref.get()
		if not doc.exists:
			return flask.render_template('login.html', fail=True)
		doc_dict = doc.to_dict()
		password_exist = doc_dict[u'password']
		if password != password_exist:
			return flask.render_template('login.html', fail=True)
		return flask.redirect(flask.url_for('waifu_page'))
	else:
		return flask.render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_page():
	if flask.request.method == 'POST':
		username = flask.request.form['username']
		doc_ref = user_ref.document(username)
		doc = doc_ref.get()
		if doc.exists:
			return flask.render_template('register.html', fail=True)
		doc_ref.set({
			u'password': flask.request.form['password']
		})
		return flask.redirect(flask.url_for('main_page'))
	else:
		return flask.render_template('register.html')


@app.route('/waifu', methods=['POST', 'GET'])
def waifu_page():
	return flask.render_template('waifu.html')

if __name__ == '__main__':
	cred_obj = fb.credentials.Certificate('cred/firebasecredential.json')
	fb.initialize_app(cred_obj)

	db = firestore.client()

	user_ref = db.collection(u'users')

	app.run(host='127.0.0.1', port=8000)