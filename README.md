# Sample Django Application

A Django application with PostgreSQL database support and Gunicorn for production deployment.

## Features

- Django 5.2.8
- PostgreSQL database support
- AWS S3 storage for static and media files
- Environment variable configuration via `.env` file
- Gunicorn WSGI server for production
- Sample view displaying an image and title

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if applicable)

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   DB_NAME=sampleapp_db
   DB_USER=postgres
   DB_PASSWORD=your-password-here
   DB_HOST=localhost
   DB_PORT=5432
   
   # AWS S3 Configuration (optional - set USE_S3=True to enable)
   USE_S3=False
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=us-east-1
   ```

5. **Create PostgreSQL database**:
   ```bash
   createdb sampleapp_db
   # Or using psql:
   # psql -U postgres
   # CREATE DATABASE sampleapp_db;
   ```

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Development

### Running the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Collecting Static Files

**Local storage** (when `USE_S3=False`):
```bash
python manage.py collectstatic
```

**S3 storage** (when `USE_S3=True`):
```bash
python manage.py collectstatic --noinput
```
This will upload static files directly to your S3 bucket.

## AWS S3 Storage Configuration

This application supports AWS S3 for storing static files and media files.

### Setup

1. **Create an S3 bucket** in your AWS account:
   - Go to AWS S3 Console
   - Create a new bucket
   - Note the bucket name and region

2. **Create an IAM user** with S3 access:
   - Go to AWS IAM Console
   - Create a new user with programmatic access
   - Attach a policy with S3 permissions (e.g., `AmazonS3FullAccess` or custom policy)
   - Save the Access Key ID and Secret Access Key

3. **Configure environment variables** in `.env`:
   ```env
   USE_S3=True
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=us-east-1
   AWS_STATIC_LOCATION=static
   AWS_MEDIA_LOCATION=media
   AWS_DEFAULT_ACL=public-read
   ```

4. **Optional: Custom domain** (if using CloudFront or custom domain):
   ```env
   AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com
   ```

5. **Upload static files to S3**:
   ```bash
   python manage.py collectstatic --noinput
   ```

### S3 Bucket Policy (Optional)

If you want to make files publicly accessible, add this bucket policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

### Switching Between Local and S3 Storage

- **Use local storage**: Set `USE_S3=False` in `.env` (default)
- **Use S3 storage**: Set `USE_S3=True` and configure AWS credentials

The application will automatically use the appropriate storage backend based on the `USE_S3` setting.

## Production Deployment with Gunicorn

### Plan for Hosting

This application is configured to run with Gunicorn as the WSGI HTTP server for production deployments.

#### Step 1: Prepare the Application

1. **Set production environment variables** in `.env`:
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   
   # If using S3 for storage
   USE_S3=True
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=us-east-1
   ```

2. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```
   Note: If using S3, this will upload files to your S3 bucket.

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

#### Step 2: Start Gunicorn

**Basic command**:
```bash
gunicorn sampleapp.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**With additional options**:
```bash
gunicorn sampleapp.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

**Using the startup script**:
```bash
./start_gunicorn.sh
```

#### Step 3: Configure Reverse Proxy (Recommended)

For production, use a reverse proxy like Nginx in front of Gunicorn:

**Nginx configuration example** (`/etc/nginx/sites-available/sampleapp`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Only needed if NOT using S3 for static files
    # location /static/ {
    #     alias /path/to/sample-django/staticfiles/;
    # }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Note**: If using S3 for static files, you don't need the `/static/` location block in Nginx as files will be served directly from S3.

#### Step 4: Run as a Service (Optional)

Create a systemd service file (`/etc/systemd/system/sampleapp.service`):
```ini
[Unit]
Description=Sample Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/sample-django
Environment="PATH=/path/to/sample-django/venv/bin"
ExecStart=/path/to/sample-django/venv/bin/gunicorn \
    sampleapp.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 4 \
    --timeout 30

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sampleapp
sudo systemctl start sampleapp
```

### Gunicorn Configuration Options

- `--bind`: Address and port to bind to (default: `127.0.0.1:8000`)
- `--workers`: Number of worker processes (recommended: `(2 × CPU cores) + 1`)
- `--timeout`: Worker timeout in seconds (default: 30)
- `--access-logfile`: Access log file path (use `-` for stdout)
- `--error-logfile`: Error log file path (use `-` for stderr)
- `--log-level`: Logging level (debug, info, warning, error, critical)

### Monitoring

- Check Gunicorn process: `ps aux | grep gunicorn`
- View logs: Check the log files specified in your Gunicorn command
- Monitor with systemd: `sudo systemctl status sampleapp`

## Project Structure

```
sample-django/
├── hello/                 # Main application
│   ├── static/           # Static files
│   ├── templates/        # HTML templates
│   └── views.py          # View functions
├── sampleapp/            # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI configuration
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── start_gunicorn.sh     # Gunicorn startup script
└── manage.py             # Django management script
```

## License

[Add your license here]
