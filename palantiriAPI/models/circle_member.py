from django.db import models

class CircleMember(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE, related_name='circler_membership')
    circle = models.ForeignKey("Circle", on_delete=models.CASCADE, related_name='circle_members')
    date_joined = models.DateField()