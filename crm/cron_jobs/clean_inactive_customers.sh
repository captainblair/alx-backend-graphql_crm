#!/bin/bash

cd "$(dirname "$0")/../.."
deleted_count=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True, created_at__lt=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

echo "$(date): Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt