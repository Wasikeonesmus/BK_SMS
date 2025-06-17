# Deployment Guide for Upendo Bakery

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