from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from string import punctuation

class DigitValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _('This password must contain any digit.'),
                code='password_not_contain_any_digit'
            )

    def get_help_text(self):
        return _(
            'Your password must contain any digit.'
        )


class PunctuationValidator:
    def validate(self, password, user=None):
        if not any(char in punctuation for char in password):
            raise ValidationError(
                _('This password must contain any punctuation sign.'),
                code='password_not_contain_any_punctuation_sign'
            )

    def get_help_text(self):
        return _(
            'Your password must contain any punctuation sign.'
        )


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _('This password must contain any uppercase.'),
                code='password_not_contain_any_uppercase'
            )

    def get_help_text(self):
        return _(
            'Your password must contain any uppercase.'
        )