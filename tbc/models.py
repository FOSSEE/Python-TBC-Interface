from django.db import models
from django.contrib.auth.models import User
from PythonTBC import settings
from django.contrib.admin.models import LogEntry
from local import sitemap_path
from taggit.managers import TaggableManager

CATEGORY = (("fluid mechanics", "Fluid Mechanics"),
            ("control systems", "Control Theory & Control Systems"),
            ("chemical engineering", "Chemical Engineering"),
            ("thermodynamics", "Thermodynamics"),
            ("mechanical engineering", "Mechanical Engineering"),
            ("signal processing", "Signal Processing"),
            ("digital communications", "Digital Communications"),
            ("electrical technology", "Electrical Technology"),
            ("maths & science", "Mathematics & Pure Science"),
            ("analog electronics", "Analog Electronics"),
            ("digital electronics", "Digital Electronics"),
            ("computer programming", "Computer Programming"),
            ("others", "Others"))

GENDER = (("male", "Male"), 
          ("female", "Female"))

COURSES = (("mtech", "M.Tech"),
           ("me", "ME"),
           ("msc", "MSc"),
           ("mscit", "MScIT"),
           ("mca", "MCA"),
           ("btech", "B.Tech"),
           ("be", "BE"),
           ("bca", "BCA"),
           ("bscit", "BScIt"),
           ("others", "Others"))
           
ABOUT_PROJ = (("pythontbc website", "Python TBC Website"),
              ("friend", "Through Friend"),
              ("prof/teacher", "Through Prof/Teacher"),
              ("mailing list", "Through Mailing List"),
              ("posters in college", "Through Posters in College"),
              ("others", "Others"))
              
PROPOSAL_STATUS = (("pending","Pending"),
                   ("samples","Samples"),
                   ("sample submitted", "Sample Submitted"),
                   ("sample disapproved", "Sample Disapproved"),
                   ("sample resubmitted", "Sample Resubmitted"),
                   ("book alloted","Book Alloted"),
                   ("codes submitted", "Codes Submitted"),
                   ("codes disapproved", "Codes Disapproved"),
                   ("book completed","Book Completed"),
                   ("rejected","Rejected"))

BOOK_PREFERENCE = (("book1","1st Book"),
                   ("book2","2nd Book"),
                   ("book3","3rd Book"))


def get_notebook_dir(instance, filename):
    book_dir = instance.book.title.replace(' ', '_')+'_by_'+instance.book.author.replace(' ','_')
    return '%s/%s' % (book_dir, filename.replace(' ', '_'))


def get_image_dir(instance, filename):
    book_dir = instance.book.title.replace(' ', '_')+'_by_'+instance.book.author.replace(' ','_')
    return '%s/screenshots/%s' % (book_dir, filename.replace(' ', '_'))


def get_sample_dir(instance, filename):
    user_name = instance.proposal.user.user.first_name+instance.proposal.user.user.last_name
    return 'sample_notebooks/%s/%s' % (user_name, filename.replace(' ', '_'))

class Profile(models.Model):
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
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    category = models.CharField(max_length=32, choices=CATEGORY)
    publisher_place = models.CharField(max_length=150)
    isbn = models.CharField(max_length=50)
    edition = models.CharField(max_length=15)
    year_of_pub = models.CharField(max_length=4)
    no_chapters = models.IntegerField(max_length=2, default=0, blank=True)
    contributor = models.ForeignKey(Profile)
    reviewer = models.ForeignKey(Reviewer)
    approved = models.BooleanField(default=False)
    tags = TaggableManager()
    def __unicode__(self):
        name = self.title or 'Book'
        return '%s'%(name)

        
class Chapters(models.Model):
    name = models.CharField(max_length=200)
    notebook = models.FileField(upload_to=get_notebook_dir)
    book = models.ForeignKey(Book)
    screen_shots = models.ManyToManyField('ScreenShots')
    def __unicode__(self):
        name = self.name or 'Chapter'
        return '%s'%(name)
    def get_absolute_url(self):
        return sitemap_path+str(self.notebook)


class ScreenShots(models.Model):
    caption = models.CharField(max_length=128)
    image = models.FileField(upload_to=get_image_dir)
    book = models.ForeignKey(Book)
    def __unicode__(self):
        name = self.caption or 'ScreenShots'
        return '%s'%(name)
        

class TempBook(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    category = models.CharField(max_length=32, choices=CATEGORY)
    publisher_place = models.CharField(max_length=150)
    isbn = models.CharField(max_length=50)
    edition = models.CharField(max_length=15)
    year_of_pub = models.CharField(max_length=4)
    no_chapters = models.IntegerField(max_length=2)
    def __unicode__(self):
        name = self.title or 'Book'
        return '%s'%(name)
        

class Proposal(models.Model):
    user = models.ForeignKey(Profile)
    textbooks = models.ManyToManyField(TempBook, related_name="proposed_textbooks")
    accepted = models.ForeignKey(Book, related_name="approved_textbook", blank=True,null=True)
    status = models.CharField(max_length=20, default="Pending", choices=PROPOSAL_STATUS)
    remarks = models.CharField(max_length=1000)
    def __unicode__(self):
        user = self.user.user.username or 'User'
        return '%s'%(user)
        
        
class SampleNotebook(models.Model):
    proposal = models.ForeignKey(Proposal)
    name = models.CharField(max_length=40)
    sample_notebook = models.FileField(upload_to=get_sample_dir)
    def __unicode__(self):
        notebook = self.proposal.accepted.title or 'notebook'
        return '%s'%(notebook)


class ActivityLog(LogEntry):
    proposal_id = models.IntegerField(null=True)
    conversation = models.TextField(null=True)


class AicteBook(models.Model):
    title = models.TextField()
    author = models.CharField(max_length=300L)
    category = models.CharField(max_length=32L)
    publisher_place = models.CharField(max_length=200L)
    isbn = models.CharField(max_length=50L)
    edition = models.CharField(max_length=15L)
    year_of_pub = models.CharField(max_length=4L)
    proposed = models.BooleanField(default=False)
    def __unicode__(self):
        notebook = self.title or 'Book'
        return '%s'%(notebook)
