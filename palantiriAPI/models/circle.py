from django.db import models

class Circle(models.Model):
    circler = models.ForeignKey("Circler", on_delete=models.CASCADE, related_name="circle_info")
    name = models.CharField(max_length=75)

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value