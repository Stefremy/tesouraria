"""
Example Tesouraria Application
This is a simple Flask application that demonstrates the deployment setup.
Replace this with your actual application code.
"""

from flask import Flask, jsonify
import os
from health_check import add_health_check

app = Flask(__name__)

# Add health check endpoint
add_health_check(app)

@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({
        'message': 'Welcome to Tesouraria - Personal Finance Management',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/status')
def status():
    """Status endpoint."""
    return jsonify({
        'application': 'Tesouraria',
        'environment': os.getenv('NODE_ENV', 'development'),
        'port': os.getenv('PORT', '8080')
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('NODE_ENV', 'development') != 'production'
    
    print(f"Starting Tesouraria on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Environment: {os.getenv('NODE_ENV', 'development')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
