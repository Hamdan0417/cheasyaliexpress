from flask import Flask, render_template, request, redirect
import requests
import json
import os
from dotenv import load_dotenv
import time
import hmac
import hashlib

load_dotenv()

app = Flask(__name__)

# Replace with your actual App Key and App Secret
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
CALLBACK_URL = 'https://127.0.0.1:5000/callback'  # Make sure this matches your app settings
API_URL = 'https://api-sg.aliexpress.com/rest'

def sign(params, secret):
    sorted_params = sorted(params.items())
    basestring = ""
    # The signature algorithm requires the method path to be included
    # if it's a new API. We can identify this by the presence of "/"
    if 'method' in params and '/' in params['method']:
        basestring += params['method']

    for k, v in sorted_params:
        if k != 'method': # The method is already added to the basestring
            basestring += f"{k}{v}"

    h = hmac.new(secret.encode('utf-8'), basestring.encode('utf-8'), hashlib.sha256)
    return h.hexdigest().upper()

def get_recommended_products(access_token):
    method = 'aliexpress.ds.recommend.feed.get'
    params = {
        'app_key': APP_KEY,
        'session': access_token,
        'method': method,
        'sign_method': 'sha256',
        'timestamp': str(int(time.time() * 1000)),
        'feed_name': 'topselling_list', # A common feed name
        'target_currency': 'USD',
        'target_language': 'en',
        'page_size': '10',
        'page_no': '1',
        'simplify': 'true'
    }

    params['sign'] = sign(params, APP_SECRET)

    response = requests.post(f"{API_URL}", params=params)

    if response.status_code == 200:
        data = response.json()
        if 'aliexpress_ds_recommend_feed_get_response' in data:
            return data['aliexpress_ds_recommend_feed_get_response']['result']
        else:
            return {'error': 'Failed to fetch products', 'details': data}
    else:
        return {'error': 'Failed to fetch products', 'details': response.text}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    authorization_url = f'https://oauth.aliexpress.com/authorize?response_type=code&client_id={APP_KEY}&redirect_uri={CALLBACK_URL}&sp=ae'
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code provided.'

    token_url = f"{API_URL}/auth/token/create"
    params = {
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': CALLBACK_URL
    }

    # The token URL requires signing as well.
    # The signature logic for token creation is slightly different
    # as it does not include the 'method' in the basestring

    token_params = {
        'app_key': APP_KEY,
        'code': code,
        'sign_method': 'sha256',
        'timestamp': str(int(time.time() * 1000)),
    }

    # I will need to find the correct signing method for token creation
    # For now, I will try with the same signing method as the other calls.

    token_url = 'https://api-sg.aliexpress.com/rest/auth/token/create'
    payload = {
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': CALLBACK_URL
    }

    token_response = requests.post(token_url, data=payload)

    if token_response.status_code == 200:
        token_data = token_response.json()
        if 'access_token' in token_data:
            access_token = token_data['access_token']
            products_data = get_recommended_products(access_token)
            return render_template('products.html', products=products_data)
        else:
            return f'Error: Could not retrieve access token. Response: {token_data}'
    else:
        return f'Error getting token: {token_response.text}'

if __name__ == '__main__':
    context = ('certs/cert.pem', 'certs/key.pem')
    app.run(debug=True, ssl_context=context)
