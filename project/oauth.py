from rauth import OAuth2Service
import json
import requests
import random
import string
from flask import current_app,redirect,session,url_for,request,abort,jsonify



def jsondecoder(content):
    new_data = data.decode('utf-8','strict')
    return json.loads(new_data)


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.state = ''.join(random.choice(string.ascii_uppercase) for i in range(10))

    def authorize(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    def callback(self):
        pass

    def validate_oauth2callback(self):
        if 'code' not in request.args: #dump request if problem
            abort(500, 'oauth2 callback: code not in request.args: \n' + str(request.__dict__))
        if request.args.get('state') != session.get('state'):
            abort(500, 'oauth2 callback: state does not match: \n' + str(request.__dict__))

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GitHubSignIn(OAuthSignIn):  
    def __init__(self):
        super(GitHubSignIn, self).__init__('github')
        self.service = OAuth2Service(
            name='github',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            base_url='https://api.github.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                state=self.state,
                redirect_uri=self.get_callback_url())
            )

    def callback(self):
        self.validate_oauth2callback()
        #get token
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'redirect_uri': self.get_callback_url()},
        )
        me = oauth_session.get('user').json()
        social_id = 'github$' + str(me['id'])
        nickname = me['login']
        email = None
        url = 'https://github.com/' + me['login'] 
        return (social_id, nickname, email, url, me)

def automatic_refresh():
    token = session['oauth_token']
    token['expires_at'] = time() - 10

    extra = {
        'client_id': "47f92ab628588bc22769",
        'client_secret': "b5da0114e0c6f50c3cc0c88b7968fa69aac1b092",
    }
    def token_updater(token):
        session['oauth_token'] = token
    github = OAuth2Service(client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)
    jsonify(github.get('https://api.github.com/user').json())
    return jsonify(session['oauth_token'])







