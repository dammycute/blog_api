from django.db import models
import uuid
from django.contrib.auth.models import User
import readtime

# Create your models here.
class Tag(models.Model):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_read_time(self):
        result = readtime.of_text(self.content)
        return result.text
    
    class Meta:
        ordering = ['-created_at']



        
        
    