import os
from django.core.exceptions import ValidationError


def validate_video_format(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый формат видео')
