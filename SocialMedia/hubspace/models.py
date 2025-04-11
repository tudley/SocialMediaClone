from django.db import models

# Create your models here.

class Profile(models.Model):
    username = models.CharField( max_length=10)
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=10)
    birthDate = models.DateField()
    biography = models.CharField(max_length=100)
    joindate = models.DateTimeField(auto_now_add = True)

    # list of followers/following
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # I should be able to get the 'following' list from the followers list, somehow...
    #following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    # config (profile pic, )
    profilePicture = models.ForeignKey("Picture", on_delete=models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"




class Message(models.Model):
    """a piece of text, sent by a profile, to another profile."""
    text = models.CharField(max_length=200)
    recipient = models.ForeignKey(Profile, related_name='recieved_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sent_messages', on_delete=models.CASCADE)
    timeSent = models.DateTimeField("date published")

    def __str__(self):
        return f"message from {self.sender} + to {self.recipient} at {self.timeSent}"

class Picture(models.Model):
    """A post, containing a picture and a small charfield, belonging to a profile"""
    file = models.ImageField(upload_to='pictures/')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datePublished = models.DateTimeField("date published")
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"Picture uploaded by {self.author} uploaded at {self.datePublished}"
    
class Post(models.Model):
    """A post, containing text, belonging to a profile"""
    text = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    datepublished = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author} at {self.datepublished}"

class Comment(models.Model):
    """A small text field, belonging to a post and an author"""
    text = models.TextField()
    datepublished = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Comment made by {self.author} on {self.post.author}s post"


class Like(models.Model):
    """A reaction to a post, owned by a post and a liker"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} liked {self.post} at {self.timestamp}"