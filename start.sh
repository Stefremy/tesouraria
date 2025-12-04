#!/bin/bash
# Startup script for Tesouraria application

set -e

echo "🚀 Starting Tesouraria application..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default port if not specified
PORT=${PORT:-8080}

# Start the application based on what's available
if [ -f main.py ]; then
    echo "Starting Python application (main.py)..."
    python main.py
elif [ -f app.py ]; then
    echo "Starting Python application (app.py)..."
    python app.py
elif [ -f simple_server.py ]; then
    echo "Starting simple Python HTTP server..."
    python simple_server.py
elif [ -f manage.py ]; then
    echo "Starting Django application..."
    python manage.py runserver 0.0.0.0:$PORT
elif [ -f server.js ]; then
    echo "Starting Node.js application (server.js)..."
    node server.js
elif [ -f index.js ]; then
    echo "Starting Node.js application (index.js)..."
    node index.js
elif [ -f package.json ]; then
    echo "Starting Node.js application (npm start)..."
    npm start
else
    echo "❌ No entry point found!"
    echo "Please create one of: main.py, app.py, simple_server.py, server.js, index.js"
    exit 1
fi
