# Tesouraria
Tesouraria Gilberto - Personal Finance Management System

## Overview
Tesouraria is a personal finance management application designed to help you track your income, expenses, and financial goals.

## Quick Start

### Using Docker (Recommended)
```bash
docker build -t tesouraria .
docker run -p 8080:8080 tesouraria
```

Or use Docker Compose:
```bash
docker-compose up
```

### Manual Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run the deployment script:
```bash
./deploy.sh
```
4. Start the application:
```bash
./start.sh
```

## Deployment

This application is ready to deploy to multiple platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy Options

**Heroku**
```bash
heroku create tesouraria-app
git push heroku main
```

**Railway**
```bash
railway init
railway up
```

**Docker Hub**
```bash
docker build -t yourusername/tesouraria .
docker push yourusername/tesouraria
```

## Configuration

1. Copy `.env.example` to `.env`
2. Update the configuration values
3. Set required environment variables for your deployment platform

## CI/CD

GitHub Actions workflows are configured for automatic deployment:
- Runs tests on pull requests
- Builds Docker images on push to main
- Deploys to configured platforms automatically

## Documentation

- [Deployment Guide](DEPLOYMENT.md) - Comprehensive deployment instructions
- [Environment Variables](.env.example) - Configuration options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.
