from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    # link each profile to a single user
    # on_delete = models.CASCADE means if the associated field (user, in this case) is deleted, all profiles associated with it are also deleted
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE) 
    
    # basic datafields for the profile
    username = models.CharField( max_length=10)
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=10)
    birthDate = models.DateField()
    joindate = models.DateTimeField(auto_now_add = True)
    gender = models.BooleanField('male=true', default=True, blank=True)

    # followers relationship is a many to many, with the 'to' argument pointing to 'self', objects of the same type as this, a Profile
    # symetrical is set to false, meaning when one profile follows another, the followed profile doesnt follow back instantly
    # related name means 
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # config (profile pic, )
    profilePicture = models.ForeignKey("Picture", on_delete=models.SET_NULL, null = True, blank = True)
    biography = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def isfollowing(self, other_profile):
        return self.following.filter(id=other_profile.id).exists()
    
    def follow(self, other_profile):
        """Add a profile to your followers list"""
        if other_profile != self:
            self.following.add(other_profile)
            
    def unfollow(self, other_profile):
        """Add a profile to your followers list"""
        self.following.remove(other_profile)
        

class Message(models.Model):
    """a piece of text, sent by a profile, to another profile."""
    # 2 important ForeignKey relationships for 'Message' the Author and recipient. the only 2 profiles that can see the message
    # here the related name shwows clearly, a messaege in relation to the author is called a sent message, and similar for a recipient
    recipient = models.ForeignKey(Profile, related_name='recieved_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, related_name='sent_messages', on_delete=models.CASCADE)

    # content of the message and metadata
    text = models.CharField(max_length=200)
    timeSent = models.DateTimeField("date published")

    def __str__(self):
        return f"message from {self.sender} + to {self.recipient} at {self.timeSent}"
    
    
class Page(models.Model):
    """A page is a public forum where members are free to post to this forum"""
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Post(models.Model):
    """A post, containing text, belonging to a profile"""
    text = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    datepublished = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Post by {self.author} at {self.datepublished}"#
    
class Picture(models.Model):
    """A post, containing a picture and a small charfield, belonging to a profile"""
    file = models.ImageField(upload_to='pictures/')
    author = models.ForeignKey(Profile, related_name='pictures', on_delete=models.CASCADE)
    datePublished = models.DateTimeField("date published", auto_now_add=True)
    caption = models.CharField(max_length=100)    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)       

    def __str__(self):
        return f"Picture uploaded by {self.author} uploaded at {self.datePublished}"


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