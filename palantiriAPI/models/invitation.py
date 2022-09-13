from django.db import models

class Invitation(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE, related_name="circle_invites")
    circle = models.ForeignKey("Circle", on_delete=models.CASCADE, related_name='circle_invitees')