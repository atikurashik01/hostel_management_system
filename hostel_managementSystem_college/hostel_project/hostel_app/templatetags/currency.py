from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter
def bdt(value):
    """Format a number as Bangladeshi Taka with symbol ৳ and two decimals.

    Usage: {{ amount|bdt }} -> ৳1,234.00
    """
    if value is None:
        return ''
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError):
        return value
    # Format with comma as thousands separator and two decimal places
    return f"৳{d:,.2f}"
