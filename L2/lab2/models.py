from django.db import models


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return "User: {} {}".format(self.email, self.password)
