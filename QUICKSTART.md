# Quick Start Guide - Tesouraria Deployment

This is a quick reference guide to get your Tesouraria application deployed quickly.

## Test Locally (No Installation Required)

The repository includes a simple demonstration server that requires no dependencies:

```bash
# Start the simple server
python3 simple_server.py

# Test it
curl http://localhost:8080/
curl http://localhost:8080/health
```

## Deploy in 5 Minutes

### Option 1: Railway (Easiest)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects the configuration
5. Done! Your app is deployed

### Option 2: Render
1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Render auto-detects Dockerfile
5. Click "Create Web Service"
6. Done!

### Option 3: Heroku
```bash
# Install Heroku CLI first
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### Option 4: Docker (Any Platform)
```bash
# Build
docker build -t tesouraria .

# Run locally
docker run -p 8080:8080 tesouraria

# Or use docker-compose
docker-compose up
```

## Adding Your Application Code

Replace `simple_server.py` or create one of these files:

**For Python:**
- `main.py` - Your main application file
- `app.py` - Flask/FastAPI application
- `requirements.txt` - Python dependencies

**For Node.js:**
- `server.js` or `index.js` - Your server file
- `package.json` - Node dependencies

The deployment configuration will automatically detect and run your application!

## Environment Variables

1. Copy the example:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
```bash
PORT=8080
NODE_ENV=production
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

3. On deployment platforms, set these in their dashboard/settings.

## Health Check

All deployment configurations expect a `/health` endpoint:

**Python (Flask):**
```python
from health_check import add_health_check
app = Flask(__name__)
add_health_check(app)
```

**Python (FastAPI):**
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

**Node.js:**
```javascript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});
```

## Troubleshooting

**Container won't start?**
- Check logs: `docker logs container-name`
- Verify `.env` file exists and is configured

**Port issues?**
- Make sure PORT environment variable is set
- Default is 8080

**Dependencies missing?**
- Check `requirements.txt` or `package.json`
- Run `./deploy.sh` to install dependencies

## Need More Help?

- See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive instructions
- Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for production readiness
- Review platform-specific documentation

## Commands Cheat Sheet

```bash
# Local development
./start.sh                    # Start the application
make run                      # Alternative using Makefile

# Deployment
./deploy.sh                   # Run deployment script
make deploy                   # Alternative using Makefile

# Docker
make docker-build             # Build Docker image
make docker-run               # Run Docker container
docker-compose up             # Start with docker-compose

# Health check
make check-health             # Check if app is running
curl http://localhost:8080/health

# Cleanup
make clean                    # Clean build artifacts
```

## Example Deployment Flow

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/tesouraria.git
cd tesouraria
cp .env.example .env

# 2. Add your code (or test with included simple_server.py)
# Edit .env with your configuration

# 3. Test locally
./start.sh
# or
python3 simple_server.py

# 4. Test with Docker
docker build -t tesouraria .
docker run -p 8080:8080 --env-file .env tesouraria

# 5. Deploy to platform
# Railway: Connect repo in dashboard
# Heroku: git push heroku main
# Render: Connect repo in dashboard
```

That's it! Your application is ready to deploy. 🚀
