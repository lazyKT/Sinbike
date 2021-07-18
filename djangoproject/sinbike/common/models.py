from django.db import models

# Create your models here.
class FAQ(models.Model):
    postname = models.CharField(max_length=100)
    contents = models.TextField()

    def __str__(self):
        return self.postname