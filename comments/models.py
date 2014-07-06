from django.db import models

class Comment(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    book = models.CharField(max_length=200)
    chapter = models.CharField(max_length=10)
    example = models.CharField(max_length=10)
    page = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    body = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

