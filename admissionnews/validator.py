from django.core.exceptions import ValidationError
import string

class SpecialCharValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if not password.isalpha():
            raise ValidationError(
                _("This username is not accpted."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Your username can't have any digit or special character.")