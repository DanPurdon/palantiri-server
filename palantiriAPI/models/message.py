from django.db import models

class Message(models.Model):
    circle = models.ForeignKey("Circle", on_delete=models.CASCADE, related_name='circle_messages')
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE)
    content = models.TextField()
    date_sent = models.DateField()
