from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/items/tag/{self.slug}/'

class Maker(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    address = models.TextField()
    number = models.CharField(max_length=20)
    nation = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_abolute_url(self):
        return f'/items/maker/{self.name}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_abolute_url(self):
        return f'/items/category/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    price = models.IntegerField()

    head_image = models.ImageField(upload_to='items/images/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    maker = models.ForeignKey(Maker, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.maker}'

    def get_absolute_url(self):
        return f'/items/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'