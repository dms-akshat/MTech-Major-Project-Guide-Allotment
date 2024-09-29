# validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code='password_too_short',
            )

        if not re.search(r'[A-Za-z]', password):
            raise ValidationError(
                _("Password must contain at least one letter."),
                code='password_no_letter',
            )

        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )

        if not re.search(r'[\W_]', password):  # \W matches any non-alphanumeric character
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, and include at least one letter, one digit, and one special character."
        )
