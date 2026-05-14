from datetime import datetime, timedelta
from django.utils import timezone

def get_date_range(days=30):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def format_date(date):
    return date.strftime('%d/%m/%Y')

def format_datetime(dt):
    return dt.strftime('%d/%m/%Y %H:%M')
