from django.db import models

class Circle(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE, related_name="circler_circle")
    name = models.CharField(max_length=75)