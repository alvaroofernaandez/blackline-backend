from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    can_receive_emails = models.BooleanField(default=True)

    def __str__(self):
        return self.name

