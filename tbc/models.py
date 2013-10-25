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

COURSES = (("mtech", "Mtech"),
           ("me", "ME"),
           ("msc", "MSc"),
           ("mscit", "MScIT"),
           ("mca", "MCA"),
           ("be", "BE"),
           ("bca", "BCA"),
           ("bscit", "BScIt"),
           ("others", "Others"))
           
ABOUT_PROJ = (("pythontbc website", "PythonTBC Website"),
              ("through friend", "Through Friend"),
              ("through prof/teacher", "Through Prof/Teacher"),
              ("through mailing list", "Through Mailing List"),
              ("through posters in college", "Through Posters in College"),
              ("others", "Others"))

def get_notebook_dir(instance, filename):
    return '%s/%s/%s' % (instance.book.contributor, instance.book.name, filename)


def get_image_dir(instance, filename):
    return '%s/%s/screenshots/%s' % (instance.book.contributor, instance.book.name, filename)


class Profile(models.Model):
    """Model to store profile of a user."""
    user = models.ForeignKey(User)
    about = models.CharField(max_length=256)
    insti_org = models.CharField(max_length=128)
    course = models.CharField(max_length=10, choices=COURSES)
    dept_desg = models.CharField(max_length=32)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone_no = models.CharField(max_length=15)
    about_proj = models.CharField(max_length=50, choices=ABOUT_PROJ)
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
    title = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    category = models.CharField(max_length=32, choices=CATEGORY)
    publisher_place = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    edition = models.CharField(max_length=15)
    year_of_pub = models.CharField(max_length=4)
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
