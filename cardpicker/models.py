# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Card(models.Model):
    dbf_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    player_class = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name
