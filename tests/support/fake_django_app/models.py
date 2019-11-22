from django.db import models


class TestModel(models.Model):
    id = models.AutoField(primary_key=True)
    some_integer = models.IntegerField()
