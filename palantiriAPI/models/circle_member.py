from django.db import models

class CircleMember(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE)
    circle = models.ForeignKey("Circle", on_delete=models.CASCADE)
    date_joined = models.DateField()