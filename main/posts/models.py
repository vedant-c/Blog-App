from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from tinymce.models import HTMLField

User=get_user_model()

class Author(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    author=models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100)
    overview=models.TextField()
    content=HTMLField()
    categories=models.ManyToManyField(Category)
    timestamp=models.DateTimeField(auto_now_add=True)
    thumbnail=models.ImageField(null=True)
    comment_count=models.IntegerField(default=0)
    view_count=models.IntegerField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse('post_update', kwargs={'id':self.id})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'id':self.id})

    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
    
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username