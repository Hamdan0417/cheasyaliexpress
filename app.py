from flask import Flask, render_template, request, redirect
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace with your actual App Key and App Secret
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
CALLBACK_URL = 'http://127.0.0.1:5000/callback'  # Make sure this matches your app settings

def get_recommended_products(access_token):
    # This is a placeholder function.
    # Replace with the actual API endpoint and parameters.
    api_url = "https://api-sg.aliexpress.com/rest/api/..."

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        # Add any required parameters here
    }

    # response = requests.get(api_url, headers=headers, params=params)
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     return {'error': 'Failed to fetch products', 'details': response.text}

    # For now, return some dummy data
    return {
        "products": [
            {"name": "Product 1", "price": "10.00"},
            {"name": "Product 2", "price": "20.00"},
            {"name": "Product 3", "price": "30.00"}
        ]
    }


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
        access_token = token_response.json().get('access_token')
        if access_token:
            products_data = get_recommended_products(access_token)
            return render_template('products.html', products=products_data)
        else:
            return 'Error: Could not retrieve access token.'
    else:
        return f'Error getting token: {token_response.text}'

if __name__ == '__main__':
    app.run(debug=True)
