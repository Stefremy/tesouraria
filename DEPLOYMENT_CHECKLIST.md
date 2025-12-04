# Deployment Checklist

## Pre-Deployment

- [ ] Code is tested and working locally
- [ ] All tests pass
- [ ] Environment variables are documented in `.env.example`
- [ ] Sensitive data is not hardcoded
- [ ] Database migrations are ready (if applicable)
- [ ] Dependencies are up to date
- [ ] `.gitignore` excludes sensitive files
- [ ] README.md is updated with deployment instructions

## Configuration

- [ ] Copy `.env.example` to `.env`
- [ ] Set `SECRET_KEY` to a random value
- [ ] Configure `DATABASE_URL` if using a database
- [ ] Set `PORT` (default: 8080)
- [ ] Configure any required API keys
- [ ] Set `NODE_ENV=production` or equivalent

## Platform-Specific Setup

### Docker
- [ ] Dockerfile builds successfully
- [ ] Docker image runs without errors
- [ ] Health check is working
- [ ] Volume mounts are configured for persistent data

### Heroku
- [ ] Heroku app created
- [ ] Procfile is configured correctly
- [ ] Environment variables set in Heroku dashboard
- [ ] Add-ons configured (database, Redis, etc.)
- [ ] Custom domain configured (if needed)

### Railway/Render
- [ ] Project created on platform
- [ ] GitHub repository connected
- [ ] Environment variables configured
- [ ] Start command configured correctly

### VPS (DigitalOcean, AWS EC2, etc.)
- [ ] SSH access configured
- [ ] Firewall rules set up
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Systemd service file installed
- [ ] Nginx/Apache reverse proxy configured

## CI/CD Setup

- [ ] GitHub Actions secrets configured
  - [ ] `DOCKER_USERNAME` and `DOCKER_PASSWORD`
  - [ ] Platform API keys (Heroku, Railway, etc.)
- [ ] Workflows are enabled
- [ ] Test deployment to staging environment
- [ ] Auto-deployment to production configured

## Security

- [ ] HTTPS/TLS enabled
- [ ] Environment variables secured (not in repository)
- [ ] Database credentials are strong
- [ ] API keys are rotated
- [ ] CORS configured appropriately
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] Input validation implemented
- [ ] SQL injection protection in place
- [ ] XSS protection enabled

## Monitoring & Logging

- [ ] Application logs configured
- [ ] Error tracking set up (Sentry, etc.)
- [ ] Uptime monitoring configured
- [ ] Performance monitoring enabled
- [ ] Database backup automated
- [ ] Health check endpoint working

## Post-Deployment

- [ ] Application is accessible at the URL
- [ ] Health check endpoint responds correctly
- [ ] Database connection is working
- [ ] All features are functional
- [ ] SSL certificate is valid
- [ ] Monitoring alerts are configured
- [ ] Documentation is updated
- [ ] Team is notified of deployment

## Rollback Plan

- [ ] Previous version can be redeployed quickly
- [ ] Database backup is available
- [ ] DNS can be switched back if needed
- [ ] Rollback procedure is documented

## Production Readiness

- [ ] Load testing completed
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan documented
- [ ] Support contacts documented
- [ ] User documentation updated
