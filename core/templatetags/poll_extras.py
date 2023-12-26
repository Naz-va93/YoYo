from decimal import Decimal
from datetime import date, timedelta

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return Decimal(value) * Decimal(len(arg))
    except (ValueError, TypeError):
        return ""


@register.filter
def multiply_by_0_15(value):
    result = str(Decimal(len(value)) * Decimal('0.15'))
    return result[:4]


@register.filter
def date_to_days(value):
    if isinstance(value, date):
        today = date.today()
        diff = today - value
        return diff.days
    return value


@register.filter
def time_since(value):
    current_time = timezone.now()

    if isinstance(value, timezone.datetime):
        time_difference = current_time - value
    else:
        time_difference = current_time - timezone.make_aware(
            timezone.datetime.combine(value, timezone.datetime.min.time()))

    if time_difference.days < 1:
        if time_difference.total_seconds() < 60:
            seconds = int(time_difference.total_seconds())
            return f"{seconds} seconds ago"

        if time_difference.total_seconds() < 3600:
            minutes = int(time_difference.total_seconds() // 60)
            return f"{minutes} minutes ago"

        hours = int(time_difference.total_seconds() // 3600)
        return f"{hours} hours ago"
    else:
        days = time_difference.days
        return f"{days} days ago"
