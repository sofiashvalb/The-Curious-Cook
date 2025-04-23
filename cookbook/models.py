from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    categoryname_ru = models.CharField(max_length=100, blank=True, null=True)
    categoryname_he = models.CharField(max_length=100, blank=True, null=True)
    categoryname_es = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.categoryname}"
    
class Card(models.Model):
    filename = models.CharField(max_length=100, default='SOME STRING')
    title = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100, blank=True, null=True)
    title_he = models.CharField(max_length=100, blank=True, null=True)
    title_es = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=10000)
    categories = models.ManyToManyField(Category, related_name='cards')
    liked = models.ManyToManyField(User, blank=True, related_name="liked_item")
    saved = models.ManyToManyField(User, blank=True, related_name="saved_item")
    anon_like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} in category {', '.join([category.categoryname for category in self.categories.all()])}"
    
    @property
    def total_likes(self):
        return self.liked.count() + self.anon_like
