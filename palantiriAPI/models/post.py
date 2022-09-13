from django.db import models

class Post(models.Model):
    circle = models.ForeignKey("Circle", on_delete=models.CASCADE, related_name="circle_posts")
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE, related_name="circler_posts")
    content = models.TextField()
    date_posted = models.DateField()
