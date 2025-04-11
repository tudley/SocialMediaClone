

from django.db import models
from .models import Profile


class Post(models.Model):
    """A post, containing text, belonging to a profile"""
    text = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    datepublished = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author} at {self.datepublished}"
    
    

class Picture(Post):
    """A post, containing a picture and a small charfield, belonging to a profile"""
    super

    file = models.ImageField(upload_to='pictures/')
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"Picture uploaded by {self.author} uploaded at {self.datePublished}"