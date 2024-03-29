from linecache import checkcache
import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.mov', '.jpeg', '.jpg', '.png', '.avi']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.\nSupported file formats: {0}').format(valid_extensions))


def validate_slug(value):
    try:
        checked_list = [None, ""]
        if value in checked_list:
            raise ValidationError(_('This field cannot be %s')%(value))
    except:
        pass
    return value
