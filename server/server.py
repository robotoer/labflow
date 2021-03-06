import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
# https://github.com/noirbizarre/flask-restplus/issues/565#issuecomment-562610603
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


# Configuration ---------------------------------------------------------------

app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', app.config.get('SERVER_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/datalayer.db')
app.config['AUTH_PROVIDER'] = os.environ.get('AUTH_PROVIDER', 'auth0')
app.config['AUTH0_DOMAIN'] = os.environ.get('AUTH0_DOMAIN', '')
app.config['AUTH0_CLIENT_ID'] = os.environ.get('AUTH0_CLIENT_ID', '')
app.config['AUTH0_API_AUDIENCE'] = os.environ.get('AUTH0_API_AUDIENCE', '')
app.config['AUTH0_AUTHORIZATION_URL'] = os.environ.get('AUTH0_AUTHORIZATION_URL', '')
app.config['AUTH0_TOKEN_URL'] = os.environ.get('AUTH0_TOKEN_URL', '')


# API Documentation -----------------------------------------------------------

authorizations = {
    'token': {
        'type': 'oauth2',
        # 'flow': 'authorizationCode',
        'flow': 'accessCode',
        'audience': app.config['AUTH0_API_AUDIENCE'],
        'domain': app.config['AUTH0_DOMAIN'],
        'clientId': app.config['AUTH0_CLIENT_ID'],
        'authorizationUrl': app.config['AUTH0_AUTHORIZATION_URL'],
        'tokenUrl': app.config['AUTH0_TOKEN_URL'],
        'scopes': {
            'read:runs': 'Read user runs',
            'read:protocols': 'Read user protocols',
            'write:runs': 'Write to user runs',
            'write:protocols': 'Write to user protocols',
        }
    }
}
api = Api(
    app,
    title='LabFlow API',
    version='0.1.0',
    authorizations=authorizations,
)
CORS(app)


# Database --------------------------------------------------------------------

db = SQLAlchemy(app)
migrate = Migrate(app, db)
