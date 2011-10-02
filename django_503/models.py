from django.db import models
from django.utils.translation import ugettext as _

class Config(models.Model):
    key = models.CharField(_('Key'), max_length=100, unique=True)
    value = models.BooleanField(_('Value'))
