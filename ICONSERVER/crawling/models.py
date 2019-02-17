from django.db import models

class Post(models.Model):
    date = models.IntegerField(default=0)
    word = models.CharField(max_length=200)
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.word