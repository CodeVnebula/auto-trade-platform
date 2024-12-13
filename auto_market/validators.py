from django.core.exceptions import ValidationError

def validate_photo_size(photo):
    max_size = 1 * 1024 * 1024  # 1 MB
    if photo.size > max_size:
        raise ValidationError(
            f"Photo size should be less than {max_size / (1024 * 1024)} MB."
        )
