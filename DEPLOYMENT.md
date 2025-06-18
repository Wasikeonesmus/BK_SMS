# Upendo Bakery - Render Deployment Guide

## 🚨 CRITICAL: Data Persistence Issue

Your application is currently running on Render **without a PostgreSQL database**, which means:
- ❌ All data will be lost when the container restarts
- ❌ No data persistence between deployments
- ❌ SQLite database is being used (not suitable for production)

## 🔧 How to Fix Data Persistence

### Option 1: Automatic Setup (Recommended)

1. **Ensure your `render.yaml` is properly configured** (already done)
2. **Redeploy from Git repository**:
   - Go to your Render dashboard
   - Navigate to your web service
   - Click "Manual Deploy" → "Deploy latest commit"
   - Render will automatically create the PostgreSQL database

### Option 2: Manual Setup

1. **Create PostgreSQL Database**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "PostgreSQL"
   - Name: `upendo-bakery-db`
   - Plan: Free
   - Region: Same as your web service

2. **Link Database to Web Service**:
   - Go to your web service settings
   - Click "Environment" tab
   - Add environment variable:
     - Key: `DATABASE_URL`
     - Value: Copy from database service settings

3. **Redeploy Application**:
   - Click "Manual Deploy" → "Deploy latest commit"

## 📊 Monitoring Your Database

### Health Check Endpoint
Visit: `https://your-app.onrender.com/health/`

This endpoint provides:
- Database connection status
- Environment information
- Data persistence status
- Database version

### Command Line Monitoring
```bash
# Check database health
python manage.py monitor_database

# Continuous monitoring (every 60 seconds)
python manage.py monitor_database --continuous

# Custom interval (every 30 seconds)
python manage.py monitor_database --continuous --interval 30
```

### Database Setup Check
```bash
python manage.py setup_render_database
```

## 🔍 Troubleshooting

### Issue: "No DATABASE_URL found"

**Symptoms:**
- Application logs show "WARNING: No DATABASE_URL found"
- Data is lost after container restart
- Using SQLite instead of PostgreSQL

**Solutions:**
1. Check if database service exists in Render dashboard
2. Verify DATABASE_URL environment variable is set
3. Ensure database service is linked to web service
4. Redeploy application after fixing configuration

### Issue: Database Connection Failed

**Symptoms:**
- Health check shows "database: error"
- Application fails to start
- Migration errors

**Solutions:**
1. Check database service status in Render dashboard
2. Verify DATABASE_URL format is correct
3. Check if database service is in same region as web service
4. Wait for database service to fully provision (can take 5-10 minutes)

### Issue: Missing Tables

**Symptoms:**
- Application works but data is missing
- Database monitoring shows missing tables

**Solutions:**
1. Run migrations: `python manage.py migrate`
2. Check migration status: `python manage.py showmigrations`
3. Create default data: `python manage.py create_default_admin`

## 📈 Performance Monitoring

### Database Performance
- Monitor connection times via health check endpoint
- Use `monitor_database` command for detailed metrics
- Check Render dashboard for database metrics

### Application Performance
- Monitor response times via health check
- Check Render logs for performance issues
- Use Sentry for error tracking (if configured)

## 🔒 Security Considerations

### Environment Variables
- Never commit sensitive data to Git
- Use Render's environment variable system
- Rotate database passwords regularly

### Database Access
- Use Render's built-in database security
- Don't expose database credentials
- Use connection pooling for better performance

## 📝 Environment Variables

Required environment variables:
```bash
DATABASE_URL=postgres://user:password@host:port/database
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
ENVIRONMENT=production
```

Optional environment variables:
```bash
SENTRY_DSN=your-sentry-dsn
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
```

## 🚀 Deployment Checklist

Before deploying:
- [ ] `render.yaml` is properly configured
- [ ] All environment variables are set
- [ ] Database service is created and linked
- [ ] Application code is committed to Git
- [ ] Health check endpoint is accessible

After deploying:
- [ ] Health check returns 200 status
- [ ] Database connection is successful
- [ ] All migrations are applied
- [ ] Default data is created
- [ ] Application is accessible via URL

## 📞 Support

If you encounter issues:
1. Check the health check endpoint first
2. Review Render logs for errors
3. Run database monitoring commands
4. Verify environment variable configuration
5. Contact support with specific error messages

## 🔄 Continuous Deployment

For automatic deployments:
1. Connect your Git repository to Render
2. Enable auto-deploy on push
3. Set up webhook for automatic deployments
4. Monitor deployment logs for issues

---

**Remember:** Always test your database configuration locally before deploying to production!

## Render Deployment

### Prerequisites
- GitHub repository with your code
- Render account

### Environment Variables Required

Set these environment variables in your Render dashboard:

#### Required Variables:
```
SECRET_KEY=your-generated-secret-key
DEBUG=false
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Optional Variables:
```
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
SENTRY_DSN=your-sentry-dsn
ENVIRONMENT=production
```

### Deployment Steps

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure the service:**
   - **Environment**: Python
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn upendo_bakery.wsgi:application --bind 0.0.0.0:$PORT`
   - **Python Version**: 3.11.7

4. **Add Environment Variables** (as listed above)

5. **Create a PostgreSQL Database** in Render and link it to your service

6. **Deploy!**

### Files Included for Deployment

- `render.yaml` - Render configuration
- `build.sh` - Build script with Pillow handling
- `build-fallback.sh` - Fallback build without Pillow
- `requirements.txt` - Python dependencies
- `requirements-no-pillow.txt` - Dependencies without Pillow
- `upendo_bakery/settings_prod.py` - Production settings

### Troubleshooting

#### Pillow Installation Issues
If Pillow fails to install:
1. Check the build logs for specific errors
2. Try using the fallback build: change build command to `chmod +x build-fallback.sh && ./build-fallback.sh`

#### Database Issues
- Ensure DATABASE_URL is properly set
- Check that the database is accessible from your service

#### Static Files Issues
- Static files are automatically collected during build
- WhiteNoise handles static file serving

### Post-Deployment

1. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Test all functionality:**
   - Login/logout
   - Product management
   - Sales processing
   - Reports generation

3. **Monitor logs** for any errors

### Security Notes

- DEBUG is set to False in production
- SSL is enforced
- Security headers are enabled
- CSRF protection is active

### Performance Optimization

- Static files are compressed and cached
- Database queries are optimized
- Logging is configured for production

## Local Development

For local development, use:
```bash
python manage.py runserver
```

The application will use SQLite and development settings automatically. 