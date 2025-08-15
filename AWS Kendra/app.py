# This is a sample Python backend script that uses the AWS boto3 SDK
# to query an Amazon Kendra index. This script would be run on a server
# and exposed via an API endpoint that your web page can call.
#
# IMPORTANT: Never expose your AWS credentials in client-side code (like JavaScript).
# This is why the search logic is handled on the server.

import boto3
import json
import os
from flask import Flask, request, jsonify

# Replace these with your actual Kendra index ID and AWS region
KENDRA_INDEX_ID = '3bff9457-2368-42de-9ee5-f1279b0d11b2'
AWS_REGION = 'ap-south-1'

# Create a Kendra client
try:
    kendra_client = boto3.client('kendra', region_name=AWS_REGION)
except Exception as e:
    print(f"Error creating Kendra client: {e}")
    kendra_client = None

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_kendra():
    """
    Handles search requests from the front end.
    """
    if kendra_client is None:
        return jsonify({"error": "Kendra client not initialized. Check AWS credentials and region."}), 500

    try:
        data = request.json
        query_text = data.get('query')

        if not query_text:
            return jsonify({"error": "Query text is required."}), 400

        # Call the Kendra query API
        response = kendra_client.query(
            QueryText=query_text,
            IndexId=KENDRA_INDEX_ID
        )

        # You can process the response here before sending it to the client.
        # For example, you might want to extract specific fields or re-format the results.
        result_items = response['ResultItems']

        # The JSON response is what your front-end JS would parse
        return jsonify({"ResultItems": result_items})

    except Exception as e:
        print(f"An error occurred during the Kendra query: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For a real-world application, you would use a production-grade web server
    # like Gunicorn or uWSGI instead of Flask's built-in server.
    app.run(debug=True, port=5000)

