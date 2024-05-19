from django.db import models
from base.models import BaseModel

# Create your models here.
class User(BaseModel):
    name=models.CharField(max_length=50,blank=True, null=True)
    email=models.CharField(max_length=100,blank=True,null=True)
    password=models.CharField(max_length=20,blank=True,null=True)

class Blog(BaseModel):
    user= models.ForeignKey('user', related_name='user', on_delete=models.CASCADE)
    author_name=models.CharField(max_length=50,null=True,blank=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    category=models.CharField(max_length=50,null=True,blank=True)
    content=models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="image")
    comment=models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.title
    
    def count_comments(self):
        return self.comment.filter(approved=True).count()
    
    @property
    def is_popular(self):
        return self.count_comments() >= 5


class Comment(BaseModel):
    blog= models.ForeignKey('blog', related_name='blog', on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True,blank=True)
    # email=models.CharField(max_length=30,null=True,blank=True)
    # subject=models.CharField(max_length=50,null=True,blank=True)
    message=models.TextField(blank=True,null=True)

