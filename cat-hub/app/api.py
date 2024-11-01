from flask import request
from app import app
import requests


@app.route("/products")
def api():
    # Read the HOST header and make a request to the API server using the host
    host = request.headers.get('Host')
    # host = 'node_app:3000'


    # Check if the host is valid
    if 'localhost:3000' not in host:
        return {"error": "Invalid host."}

    response = requests.get(f"http://{host}/api/v1/products")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        return {"error": "Unable to fetch products."}
