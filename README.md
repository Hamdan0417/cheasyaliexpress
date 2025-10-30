# CheasyAliexpress Dropshipping Store

This is a simple dropshipping store application that connects to the AliExpress API.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add your AliExpress App Key and App Secret:
    ```
    APP_KEY=your_app_key
    APP_SECRET=your_app_secret
    ```

3.  **Generate a self-signed SSL certificate:**
    This application uses HTTPS for the callback URL. For local development, you'll need to generate a self-signed SSL certificate.
    ```bash
    mkdir certs
    openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365 -subj "/C=US/ST=California/L=Mountain View/O=Test/OU=Test/CN=localhost"
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will be running at `https://127.0.0.1:5000`.

## API Integration

The application is set up to connect to the AliExpress API using OAuth 2.0. The `get_recommended_products` function in `app.py` is a placeholder and needs to be updated with the correct API endpoint for fetching products.
