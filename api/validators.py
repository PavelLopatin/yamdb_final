from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    current = date.today()
    if value > current.year:
        raise ValidationError('Please enter the correct year')
