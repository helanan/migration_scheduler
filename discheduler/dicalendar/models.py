import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Migration(models.Model):
    migration_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date added')

    def __str__(self):
        return self.migration_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    migration = models.ForeignKey(Migration, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
