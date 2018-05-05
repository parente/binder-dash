'''
adapted from https://dash.plot.ly/getting-started

hackety hack hack

JUPYTERHUB_BASE_URL=/
JUPYTERHUB_CLIENT_ID=user-parente-binder-dash-t138krd8
JUPYTERHUB_API_TOKEN=dbc7fd2419184296b405c5a7d8157c4f
JUPYTERHUB_API_URL=http://10.15.251.161:8081/hub/api
JUPYTERHUB_USER=parente-binder-dash-t138krd8
JUPYTERHUB_OAUTH_CALLBACK_URL=/user/parente-binder-dash-t138krd8/oauth_callback
JUPYTERHUB_HOST=
JUPYTERHUB_SERVICE_PREFIX=/user/parente-binder-dash-t138krd8/

HubOAuth(
        api_token=api_token,
        api_url=self.hub_api_url,
        hub_prefix=self.hub_prefix,
        base_url=self.base_url,
    )

'''
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, url_for
from flask_oauthlib.client import OAuth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

flask_app = Flask('dash')
flask_app.secret_key = 'not that secret who cares'

api_token = os.getenv('JUPYTERHUB_API_TOKEN')
oauth_client_id = os.getenv('JUPYTERHUB_CLIENT_ID')
oauth_redirect_uri = os.getenv('JUPYTERHUB_OAUTH_CALLBACK_URL')
oauth_authorization_url = 'https://hub.mybinder.org/hub/api/oauth2/authorize' # TODO build off base url
oauth_token_url = os.getenv('JUPYTERHUB_API_URL') + '/oauth2/token'
url_base_pathname=os.getenv('JUPYTERHUB_SERVICE_PREFIX', '/')

print(locals())

oauth = OAuth()
jhub = oauth.remote_app('jupyterhub',
    access_token_url=oauth_token_url,
    authorize_url=oauth_authorization_url,
    consumer_key=oauth_client_id,
    consumer_secret=api_token
)
oauth.init_app(flask_app)

@flask_app.before_first_request
def startup():
    print('authorizing')
    # TODO: does it have to be oauth_redirect_uri?
    jhub.authorize(callback=f'localhost:8000{url_base_pathname}/oauth_authorized')

@flask_app.route(url_base_pathname+'/oauth_authorized')
def oauth_authorized(): 
    print('authorized callback')
    resp = jhub.authorized_response()
    print('resp:', resp)
    return redirect(url_base_pathname+'dash')

app = dash.Dash(server=flask_app, url_base_pathname=url_base_pathname+'/dash')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)
