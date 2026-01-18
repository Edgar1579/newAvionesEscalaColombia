from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica dos valores"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency(value):
    """Formatea un número como moneda"""
    try:
        return "${:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "$0"