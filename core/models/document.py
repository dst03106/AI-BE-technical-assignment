# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from pgvector.django import VectorField

from config.settings.env_settings import settings


class Document(models.Model):
    source_type = models.CharField()
    source_id = models.IntegerField()
    content = models.TextField()
    embedding_vector = VectorField(settings.embedding_model_dim)
    model = models.TextField()
    embedding_hash = models.CharField(unique=True, max_length=64)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = f"documents_{settings.embedding_model_dim}"
