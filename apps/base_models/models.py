from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class BaseModel(models.Model):
    created = models.ForeignKey(
        User, 
        models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name=_('created by')
    )
    modified = models.ForeignKey(
        User, 
        models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name=_('modified by')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at')
    )

    class Meta:
        abstract = True
