from django.db import models

class Post(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateField()
