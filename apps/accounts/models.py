from django.db import models
from apps.base_models import BaseModel
from  django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CompanyInfo(BaseModel):

    logo = models.ImageField(upload_to='company', verbose_name=_('Logo'), null=True, blank=True)
    phone = PhoneNumberField(region='UZ', null=True, blank=True)
    about_img = models.ImageField(upload_to="company", null=True, blank=True)
    team = models.TextField(max_length=5000, null=True)
    team_story = models.TextField(max_length=5000,null=True)

    longitude = models.DecimalField(max_digits=50, decimal_places=25, null=True, blank=True)
    latitude = models.DecimalField(max_digits=50, decimal_places=25, null=True, blank=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Company')

    def __str__(self):
        return 'Company Info'