# CRM Celery Setup

## Prerequisites

1. **Install Redis**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # macOS
   brew install redis
   
   # Windows
   # Download and install Redis from https://redis.io/download
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup Steps

1. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Start Redis Server**:
   ```bash
   redis-server
   ```

3. **Start Celery Worker** (in a new terminal):
   ```bash
   celery -A crm worker -l info
   ```

4. **Start Celery Beat** (in another new terminal):
   ```bash
   celery -A crm beat -l info
   ```

5. **Start Django Development Server**:
   ```bash
   python manage.py runserver
   ```

## Verification

- Check logs in `/tmp/crm_report_log.txt` for weekly reports
- Reports are generated every Monday at 6:00 AM
- Manual task execution: `python manage.py shell -c "from crm.tasks import generate_crm_report; generate_crm_report.delay()"`

## Report Format

Reports are logged in the format:
```
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```