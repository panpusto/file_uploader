from django.core.exceptions import ValidationError

def validate_time_to_expired(value: int) -> None:
    """Validates user input of expiration time for link to download zip."""
    MIN_TIME = 300
    MAX_TIME = 86400
    if not MIN_TIME <= value <= MAX_TIME:
        raise ValidationError("Value must be a number between 300(5 min) and 86400(24 hrs)")
