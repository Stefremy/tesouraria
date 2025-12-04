.PHONY: help install test build run deploy clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "Installing dependencies..."
	@if [ -f requirements.txt ]; then \
		python3 -m venv venv; \
		. venv/bin/activate; \
		pip install -r requirements.txt; \
	fi
	@if [ -f package.json ]; then \
		npm install; \
	fi

test: ## Run tests
	@echo "Running tests..."
	@if [ -f pytest.ini ]; then \
		. venv/bin/activate && pytest; \
	elif [ -f package.json ] && grep -q '"test"' package.json; then \
		npm test; \
	else \
		echo "No tests found"; \
	fi

build: ## Build the application
	@echo "Building application..."
	@if [ -f package.json ] && grep -q '"build"' package.json; then \
		npm run build; \
	fi

run: ## Run the application locally
	@./start.sh

deploy: ## Run deployment script
	@./deploy.sh

clean: ## Clean build artifacts and dependencies
	@echo "Cleaning..."
	@rm -rf venv/ node_modules/ __pycache__/ *.pyc dist/ build/ .pytest_cache/ .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

docker-build: ## Build Docker image
	@docker build -t tesouraria:latest .

docker-run: ## Run Docker container
	@docker run -p 8080:8080 --env-file .env tesouraria:latest

docker-compose-up: ## Start services with docker-compose
	@docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	@docker-compose down

docker-logs: ## View Docker container logs
	@docker-compose logs -f

setup-env: ## Create .env file from .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created. Please edit it with your configuration."; \
	else \
		echo ".env file already exists"; \
	fi

check-health: ## Check application health
	@curl -f http://localhost:8080/health || echo "Health check failed"

lint: ## Run linters
	@echo "Running linters..."
	@if command -v flake8 &> /dev/null; then \
		flake8 .; \
	fi
	@if command -v pylint &> /dev/null; then \
		pylint **/*.py; \
	fi
	@if [ -f package.json ] && grep -q '"lint"' package.json; then \
		npm run lint; \
	fi

format: ## Format code
	@echo "Formatting code..."
	@if command -v black &> /dev/null; then \
		black .; \
	fi
	@if [ -f package.json ] && grep -q '"format"' package.json; then \
		npm run format; \
	fi
