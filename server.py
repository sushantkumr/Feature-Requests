from flask import Flask, jsonify, request, redirect, url_for, render_template
from lib.models.feature_requests import FeatureRequest
from lib.models import db, utils
from importlib import import_module
from flask_login import login_required, current_user
from lib.models.users import User
import flask_login
import logging
from lib.core import config


configuration = config.get_config()

app = Flask(__name__)

app.secret_key = configuration['secret_key']
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

SUCCESS = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404


# ***
# Auth stuff
# ***


@login_manager.user_loader
def user_loader(id):
    """flask_login stuff."""
    user = User.query.get(id)
    if user is None:
        return
    return user


@login_manager.request_loader
def request_loader(request):
    """flask_login stuff."""
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(User.name == username).all()
    if user == []:
        return
    user = user[0]

    salt, hash = utils.hash_password(password, user.salt)
    if hash == user.hash:
        return user
    else:
        return


@app.route('/', methods=['GET'])
def root():
    """Serve the home page of the web app."""
    if current_user.__dict__.get('id', None):
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.__dict__.get('id', None):
        return render_template('login.html')

    if request.method == 'GET':
        return render_template('signup.html')

    else:
        data = request.get_json()
        username = data.get('username', '').lower()
        password = data.get('password', '')
        client = data.get('client', '')['name']
        confirm_password = data.get('confirm_password', '')

        if len(username) < 5 or len(username) > 100:
            return jsonify({
                'success': False,
                'message': 'Username should be 5 to 100 characters long.'
            })

        if len(password) < 12 or len(password) > 100:
            return jsonify({
                'success': False,
                'message': 'Password should be 12 to 100 characters long.'
            })

        if password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Passwords do not match.'
            })

        user = User.query.filter(User.name == username).first()
        if user:
            return jsonify({
                'success': False,
                'message': 'This username is taken.'
            })

        new_user = User(password=password, name=username, client=client)
        db.db_session.add(new_user)
        db.db_session.commit()
        flask_login.login_user(new_user)
        return jsonify({
            'success': True
        })


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User will be served the login page or will be logged in."""
    # import pudb; pudb.set_trace();
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username', None).lower()
        password = data.get('password', None)

        user = User.query.filter(User.name == username).first()
        if not user:
            return jsonify({
                'success': False,
                'message': 'The username or password is incorrect.'
            })
        salt, hash = utils.hash_password(password, user.salt)
        if hash == user.hash:
            flask_login.login_user(user)
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False,
                'message': 'The username or password is incorrect.'
            })


@app.route('/new_feature_request', methods=['GET', 'POST'])
@login_required
def new_feature_request():
    return render_template('new_feature_request.html')


@app.route("/delete/<int:feature_request_id>", methods=['POST', 'GET'])
@login_required
def delete_request(feature_request_id):
    FeatureRequest.query.filter(FeatureRequest.id == feature_request_id).delete()
    db.db_session.commit()
    return render_template('home.html')


@app.route("/edit", methods=['POST', 'GET'])
@login_required
def edit_request():
    return render_template('edit_feature_request.html')


@app.route('/ajax', methods=['GET', 'POST'])
@login_required
def ajax_handler():
    # import pudb; pudb.set_trace();
    origin = request.remote_addr
    logging.info('Request from {}'.format(origin))
    module = request.args.get('module')
    file = request.args.get('file')
    method = request.args.get('method')
    logging.info('Target method {}'.format(module + '/' + file + '/' + method))
    try:
        kwargs = request.get_json()
    except:
        return jsonify({
            'success': False,
            'message': 'Could not parse request JSON'
        }), BAD_REQUEST

    try:
        function = getattr(import_module('.'.join(['lib', module, file])),
                           method)
    except:
        return jsonify({
            'success': False,
            'message': 'Method not found.'
        }), NOT_FOUND

    try:
        data = function(**kwargs)
        db.db_session.commit()
        return jsonify({'success': True, 'data': data})

    except Exception as e:
        # TODO: Log errors
        # Discard all changes if an error occurs
        db.db_session.rollback()
        return jsonify({
            'success': False,
            'message': 'Unhandled exception, session rolled back.'
        }), BAD_REQUEST


@app.route('/logout')
@login_required
def logout():
    """The user is redirected to the login page after logging them out."""
    flask_login.logout_user()
    return redirect(url_for('root'))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s'
    )
    app.run(
        host='0.0.0.0',
        port=5000,
        threaded=True,
        debug=True
    )
