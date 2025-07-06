# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from core.models import CompanyNews


class Company(models.Model):
    id: str
    name = models.CharField(max_length=255)
    data = models.JSONField()

    company_news: "RelatedManager['CompanyNews']"

    class Meta:
        managed = False
        db_table = "company"
