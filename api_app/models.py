from django.db import models
from accounts.models import User

# Create your models here.



class Collective(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User)
    private = models.BooleanField(default=False)
    #image

class Post(models.Model):
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=45)
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE)
    # image = models.ForeignKey(Image, on_delete=models.SET_DEFAULT, default=None, null=True)

    def __str__(self):
        return f"{self.content}: created {self.created}"
    
class Image(models.Model):
    url = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE)
    
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    address = models.CharField(max_length=300)
    date = models.DateTimeField()
    rsvps = models.ManyToManyField(User)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}: {self.description}"
    


    def __str__(self):
        return f"Url for image: {self.url}"

    
# class Comment(models.Model):
#     content = models.TextField(max_length=1000)
#     created = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # username



