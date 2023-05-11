from django.db import models
from accounts.models import User

# Create your models here.



class Collectiv(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User)
    private = models.BooleanField(default=False)
    #image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=45)
    collectiv = models.ForeignKey(Collectiv, on_delete=models.CASCADE)
    
    # def get_username(self):
    #     postUser = User.objects.get(id=self.user)
    #     return postUser.username


    def __str__(self):
        return f"{self.title}: created {self.created}"
    
class Comment(models.Model):
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # username



