# Deployment Guide - Tesouraria

This guide explains how to deploy the Tesouraria application to various platforms.

## Prerequisites

- Git installed
- Account on your chosen deployment platform
- Application code (Python/Node.js/etc.)

## Deployment Options

### Option 1: Docker Deployment

The easiest way to deploy is using Docker, which works on any platform that supports containers.

#### Local Docker Build
```bash
# Build the Docker image
docker build -t tesouraria .

# Run the container
docker run -p 8080:8080 tesouraria
```

#### Deploy to Cloud Platforms

**Railway**
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

**Render**
1. Connect your GitHub repository to Render
2. Render will auto-detect the Dockerfile
3. Configure environment variables
4. Deploy automatically on push

**Google Cloud Run**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/tesouraria
gcloud run deploy --image gcr.io/PROJECT-ID/tesouraria --platform managed
```

**AWS ECS/Fargate**
```bash
# Authenticate Docker to Amazon ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com

# Build, tag, and push the image
docker build -t tesouraria .
docker tag tesouraria:latest aws_account_id.dkr.ecr.region.amazonaws.com/tesouraria:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/tesouraria:latest
```

### Option 2: Platform-as-a-Service (PaaS)

#### Heroku
```bash
# Login to Heroku
heroku login

# Create a new app
heroku create tesouraria-app

# Deploy
git push heroku main

# Set environment variables
heroku config:set KEY=value
```

#### Vercel (for Node.js/Next.js apps)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

#### Netlify (for static sites/JAMstack)
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Option 3: Traditional Server Deployment

For deploying to a VPS (DigitalOcean, Linode, AWS EC2, etc.):

```bash
# SSH into your server
ssh user@your-server-ip

# Clone the repository
git clone https://github.com/Stefremy/tesouraria.git
cd tesouraria

# Install dependencies (example for Python)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with a process manager (e.g., PM2 for Node.js, systemd for Python)
# See deploy.sh script for automation
```

## CI/CD Pipeline

This repository includes GitHub Actions workflows that automatically:
- Run tests on pull requests
- Deploy to production on push to main branch
- Build and push Docker images

### Setting Up GitHub Actions Deployment

1. Go to repository Settings → Secrets and variables → Actions
2. Add required secrets:
   - `DOCKER_USERNAME` and `DOCKER_PASSWORD` (for Docker Hub)
   - Platform-specific credentials (e.g., `HEROKU_API_KEY`, `RAILWAY_TOKEN`)
3. Update `.github/workflows/deploy.yml` with your deployment configuration

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Application
PORT=8080
NODE_ENV=production

# Database
DATABASE_URL=your_database_connection_string

# API Keys (if needed)
API_KEY=your_api_key

# Security
SECRET_KEY=your_secret_key
```

## Health Checks

The application exposes a health check endpoint:
- `GET /health` - Returns application status

## Monitoring and Logs

- **Docker**: `docker logs container-name`
- **Heroku**: `heroku logs --tail`
- **Railway**: Check Railway dashboard
- **Server**: Use logging service or check application logs

## Scaling

### Horizontal Scaling
- **Docker/Kubernetes**: Increase replica count
- **Heroku**: `heroku ps:scale web=3`
- **Cloud Platforms**: Adjust instance count in dashboard

### Vertical Scaling
- Upgrade to a larger instance size in your platform's dashboard

## Backup and Recovery

1. **Database Backups**: Configure automated backups in your database service
2. **Code Backups**: Git repository serves as code backup
3. **Data Backups**: Regular exports of user data

## Troubleshooting

### Container won't start
- Check Docker logs: `docker logs container-id`
- Verify environment variables are set
- Ensure port is not already in use

### Application crashes
- Check application logs
- Verify all dependencies are installed
- Ensure database connection is working

### Build fails
- Check that all required files are present
- Verify dependency versions are compatible
- Review build logs for specific errors

## Security Checklist

- [ ] Environment variables configured (not hardcoded)
- [ ] HTTPS/TLS enabled
- [ ] Database credentials secured
- [ ] API keys rotated regularly
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Dependencies updated

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review platform-specific documentation
3. Open an issue in the GitHub repository
