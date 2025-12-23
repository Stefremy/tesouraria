#!/bin/bash
# Deployment script for Tesouraria application

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        print_warning "Please edit .env file with your configuration before running the application"
    else
        print_error "No .env.example file found"
    fi
fi

# Determine the application type and install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Check for Python application
    if [ -f requirements.txt ]; then
        print_status "Python application detected"
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3 is not installed"
            exit 1
        fi
        
        # Create virtual environment if it doesn't exist
        if [ ! -d venv ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        print_status "Python dependencies installed"
    fi
    
    # Check for Node.js application
    if [ -f package.json ]; then
        print_status "Node.js application detected"
        if ! command -v npm &> /dev/null; then
            print_error "npm is not installed"
            exit 1
        fi
        
        npm install
        print_status "Node.js dependencies installed"
    fi
}

# Run database migrations if applicable
run_migrations() {
    print_status "Checking for database migrations..."
    
    # Python/Django migrations
    if [ -f manage.py ]; then
        python manage.py migrate --noinput
        print_status "Django migrations applied"
    fi
    
    # Python/Flask migrations (Alembic)
    if [ -d migrations ]; then
        if command -v alembic &> /dev/null; then
            alembic upgrade head
            print_status "Alembic migrations applied"
        fi
    fi
    
    # Node.js migrations (Sequelize, Prisma, etc.)
    if [ -f package.json ]; then
        if grep -q "prisma" package.json; then
            npx prisma migrate deploy
            print_status "Prisma migrations applied"
        fi
    fi
}

# Build the application if needed
build_application() {
    print_status "Building application..."
    
    # Check for build scripts
    if [ -f package.json ] && grep -q "\"build\"" package.json; then
        npm run build
        print_status "Application built successfully"
    fi
}

# Main deployment process
main() {
    echo "=================================="
    echo "  Tesouraria Deployment Script"
    echo "=================================="
    echo ""
    
    # Install dependencies
    install_dependencies
    
    # Run migrations
    run_migrations
    
    # Build application
    build_application
    
    echo ""
    print_status "Deployment completed successfully!"
    echo ""
    echo "To start the application:"
    echo "  - For Python: python main.py or python app.py"
    echo "  - For Node.js: npm start or node server.js"
    echo "  - Using Docker: docker build -t tesouraria . && docker run -p 8080:8080 tesouraria"
    echo ""
}

# Run main function
main
