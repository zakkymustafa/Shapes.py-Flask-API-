from rauth import OAuth2Service
import json
from flask import current_app,redirect,session,url_for,request



class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH CREDENTIALS'][provider_name]
        self.consumer_id = credentials['client_id']
        self.consumer_secret = credentials['client_secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,_external=True)

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
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url(),
            )

        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode())

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  "redirect_uri":self.get_callback_url(),
                  },

        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'github$' + me['id'],
            me.get('email').split('@')[0],  
                                            
            me.get('email')
        )
