from flask import Flask, render_template, request, jsonify
from lib.models import db, utils
import logging
from importlib import import_module
app = Flask(__name__)

SUCCESS = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404


@app.route('/', methods=['GET'])
def root():
    return render_template('home.html')


@app.route('/new_feature_request', methods=['GET', 'POST'])
def new_feature_request():
    return render_template('new_feature_request.html')


@app.route('/ajax', methods=['GET', 'POST'])
def ajaxHandler():
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
