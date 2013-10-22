from django.db import models
from django.contrib.auth.models import User
from PythonTBC import settings


CATEGORY = (("computer science", "Computer Science"),
            ("chemical engg", "Chemical Engg"),
            ("aerospace engg", "Aerospace Engg"),
            ("electronics engg", "Electronics Engg"),
            ("thermodynamics", "Thermodynamics"),
            ("mechanical engg", "Mechanical Engg"),
            ("mathematics", "Mathematics"))

GENDER = (("male", "Male"), 
          ("female", "Female"))

def get_notebook_dir(instance, filename):
    return '%s/%s/%s' % (instance.book.contributor, instance.book.name, filename)


def get_image_dir(instance, filename):
    return '%s/%s/screenshots/%s' % (instance.book.contributor, instance.book.name, filename)


class Profile(models.Model):
    """Model to store profile of a user."""
    user = models.ForeignKey(User)
    about = models.CharField(max_length=256)
    insti_org = models.CharField(max_length=128)
    dept_desg = models.CharField(max_length=32)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone_no = models.CharField(max_length=15)
    def __unicode__(self):
        name = self.user.first_name or 'Profile'
        return '%s'%(name)
        

class Reviewer(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    def __unicode__(self):
        name = self.name or 'Reviewer'
        return '%s'%(name)

class Book(models.Model):
    """Model to store the book details"""
    name = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    category = models.CharField(max_length=32, choices=CATEGORY)
    publisher = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    no_chapters = models.IntegerField(max_length=2)
    contributor = models.ForeignKey(Profile)
    reviewer = models.ForeignKey(Reviewer)
    def __unicode__(self):
        name = self.name or 'Book'
        return '%s'%(name)
        
class Chapters(models.Model):
    name = models.CharField(max_length=200)
    notebook = models.FileField(upload_to=get_notebook_dir)
    book = models.ForeignKey(Book)
    def __unicode__(self):
        name = self.name or 'Chapter'
        return '%s'%(name)


class ScreenShots(models.Model):
    caption = models.CharField(max_length=128)
    image = models.FileField(upload_to=get_image_dir)
    book = models.ForeignKey(Book)
    def __unicode__(self):
        name = self.caption or 'ScreenShots'
        return '%s'%(name)
