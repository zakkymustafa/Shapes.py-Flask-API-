from rauth import OAuth2Service
import json
import requests
import random
import string
from flask import current_app,redirect,session,url_for,request,abort



def jsondecoder(content):
    try:
        return json.loads(content.decode('utf-8'))
    except Exception:
        return json.loads(content)


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
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('user').json()
        social_id = 'github$' + str(me['id'])
        nickname = me['login']
        email = None
        url = 'https://github.com/' + me['login'] #TODO: be sure this isn't changed
        return (social_id, nickname, email, url, me)

























    # def authorize(self):
    #      request_token = self.service.get_request_token(
    #         params={'oauth_callback': self.get_callback_url()}
    #     )
    #     return redirect(self.service.get_authorize_url(
    #         scope='email',
    #         response_type='code',
    #         redirect_uri=self.get_callback_url(),
    #         )

    #     )

    # def callback(self):
    #     # def decode_json(payload):
    #     #     return json.loads(payload.decode())

    #     if 'code' not in request.args:
    #         return None, None, None
    #     oauth_session = self.service.get_auth_session(
    #         data={'code': request.args['code'],
    #               'grant_type': 'authorization_code',
    #               "redirect_uri":self.get_callback_url()},
    #         # decoder = decode_json
                  

    #     )
    #     me = oauth_session.get().json()
    #     return (
    #         'github$' + me['id'],
    #         me.get('email').split('@')[0],  
                                            
    #         me.get('email')
    #     )


# 'me?fields=id,email'