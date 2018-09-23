from django.core.exceptions import ValidationError


def validate_lowercase(value):
    if not value.islower():
        raise ValidationError(
            '%(value)s must be in lower case.',
            params={'value': value},
        )
