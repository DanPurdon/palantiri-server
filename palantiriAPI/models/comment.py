from django.db import models

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateField()
