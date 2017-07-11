from django.db import models
from django.contrib.auth.models import User
from PythonTBC import settings
from django.contrib.admin.models import LogEntry
from .local import sitemap_path
from taggit.managers import TaggableManager
from django.core.files.storage import FileSystemStorage
import os

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

YEAR = (("first", "First"),
           ("second", "Second"),
           ("third", "Third"),
           ("fourth", "Fourth"))
UNIVERSITY = (
("A.I Kalsekar Technical Campus, Mumbai University","A.I Kalsekar Technical Campus, Mumbai University"),
("AALIM MOHAMED SALEGH COLLEGE OF ENGINEERING","AALIM MOHAMED SALEGH COLLEGE OF ENGINEERING"),
("ABAL Technologies","ABAL Technologies"),
("ABES Engineering College","ABES Engineering College"),
("Acharya Narendra Dev College","Acharya Narendra Dev College"),
("Acropolis Institute of Technology & Research, Indore","Acropolis Institute of Technology & Research, Indore"),
("Adamas University","Adamas University"),
("Aggarwal public school","Aggarwal public school"),
("AIKTC, Panvel","AIKTC, Panvel"),
("AISSMS COE PUNE","AISSMS COE PUNE"),
("AKU patna","AKU patna"),
("AL AMEEN ENGINEERING COLLEGE","AL AMEEN ENGINEERING COLLEGE"),
("Alliance University","Alliance University"),
("Alpha College of Engineering & Tech., Kalol","Alpha College of Engineering & Tech., Kalol"),
("Amity University","Amity University"),
("Amrita School of Engineering, Bangalore","Amrita School of Engineering, Bangalore"),
("Andalas university","Andalas university"),
("Andhra Loyola College","Andhra Loyola College"),
("Andhra university","Andhra university"),
("Anglo Eastern ship management india Pvt. Ltd","Anglo Eastern ship management india Pvt. Ltd"),
("Anjuman -I-Islam Kalsekar Technical Campus and School of Enginering","Anjuman -I-Islam Kalsekar Technical Campus and School of Enginering"),
("Anna university","Anna university"),
("Apex institute of technology and managment","Apex institute of technology and managment"),
("APG UNIVERSITY SHIMLA","APG UNIVERSITY SHIMLA"),
("Atharva College Of Engineering","Atharva College Of Engineering"),
("Autonomous/kumaraguru college of technology coimbatore","Autonomous/kumaraguru college of technology coimbatore"),
("Ayya Nadar Janaki Ammal College,Sivakasi","Ayya Nadar Janaki Ammal College,Sivakasi"),
("B M S College of Engineering ,Bangalore","B M S College of Engineering ,Bangalore"),
("Bannari Amman Institute of Technology","Bannari Amman Institute of Technology"),
("Bapurao deshmukh college of engg.,nagpur university","Bapurao deshmukh college of engg.,nagpur university"),
("Barkatullah university","Barkatullah university"),
("BCRCE,DURGAPUR","BCRCE,DURGAPUR"),
("Bhai Gurdas Polytechnic College","Bhai Gurdas Polytechnic College"),
("Bharath university","Bharath university"),
("Bharati Vidyapeeth College of Engineering","Bharati Vidyapeeth College of Engineering"),
("Biju Patnaik University of Technology","Biju Patnaik University of Technology"),
("BIRLA INSTITUTE OF TECHNOLOGY MESRA","BIRLA INSTITUTE OF TECHNOLOGY MESRA"),
("Brahmanand institute of management & science","Brahmanand institute of management & science"),
("BVRIT Hyderabad College of Engineering For Women","BVRIT Hyderabad College of Engineering For Women"),
("Central University of Rajasthan","Central University of Rajasthan"),
("Charusat University Changa","Charusat University Changa"),
("CMR Institute of technology","CMR Institute of technology"),
("College of engineering and technology,Bhubaneswar","College of engineering and technology,Bhubaneswar"),
("COLLEGE OF ENGINEERING MUNNAR","COLLEGE OF ENGINEERING MUNNAR"),
("College of Engineering Pune","College Of Engineering Roorkee"),
("College Of Engineering Roorkee","Charusat University Changa"),
("Concordia University","Concordia University"),
("Cummins College Of Engineering for Women, Pune","Cummins College Of Engineering for Women, Pune"),
("D. D. University","D. D. University"),
("D. Y. P. I. E. T, Pimpri, Pune","D. Y. P. I. E. T, Pimpri, Pune"),
("D.J. Sanghavi College of Engineering","D.J. Sanghavi College of Engineering"),
("Deenbandhu Chhotu Ram University of Science & Technology","Deenbandhu Chhotu Ram University of Science & Technology"),
("Defence Institute of Advanced Technology,Pune","Defence Institute of Advanced Technology,Pune"),
("DELHI TECHNOLOGICAL UNIVERSITY","DELHI TECHNOLOGICAL UNIVERSITY"),
("Dev Bhoomi Group Of Institution","Dev Bhoomi Group Of Institution"),
("Dharamshinh desai university ,nadiad","Dharamshinh desai university ,nadiad"),
("Don Bosco Institute of Technology, Kurla","Don Bosco Institute of Technology, Kurla"),
("Dr. Babasaheb Ambedkar Marathwada University, Aurangabad","Dr. Babasaheb Ambedkar Marathwada University, Aurangabad"),
("Dr.Mgr Educational and research institute university","Dr.Mgr Educational and research institute university"),
("Excel Engineering College","Excel Engineering College"),
("Fr. Conceicao Rodrigues College of Engineering","Fr. Conceicao Rodrigues College of Engineering"),
("G.H.PATEL COLLEGE OF ENGINEERING AND TECHNOLOGY","G.H.PATEL COLLEGE OF ENGINEERING AND TECHNOLOGY"),
("G.L. Bajaj Group of Institutions, Mathura","G.L. Bajaj Group of Institutions, Mathura"),
("Gautam Buddha University , Greater Noida","Gautam Buddha University , Greater Noida"),
("GD Goenka University","GD Goenka University"),
("Genba Sopanrao Moze College Of Engineering","Genba Sopanrao Moze College Of Engineering"),
("GITAM University, Visakhapatnam","GITAM University, Visakhapatnam"),
("Gokaraju Rangaraju Institute of Engineering and Technology","Gokaraju Rangaraju Institute of Engineering and Technology"),
("Government College of Engineering,Salem","Government College of Engineering,Salem"),
("Government polytechnic awasari,Pune","Government polytechnic awasari,Pune"),
("Govind Ballabh Pant Engineering College, Pauri Garhwal","Govind Ballabh Pant Engineering College, Pauri Garhwal"),
("Gujarat Technical University","Gujarat Technical University"),
("Gurgaon College of Engineering","Gurgaon College of Engineering"),
("Gurunanak College","Gurunanak College"),
("Harish-Chandra Research Institute, Allahabad","Harish-Chandra Research Institute, Allahabad"),
("Heritage Institute of Technology","Heritage Institute of Technology"),
("Ideal Institute of Technology,Ghaziabad","Ideal Institute of Technology,Ghaziabad"),
("IIMT College of engineering,Gr.Noida","IIMT College of engineering,Gr.Noida"),
("Indian Institute of chemical technology","Indian Institute of chemical technology"),
("Indian Institute of Engineering Bombay","Indian Institute of Engineering Bombay"),
("Indian Institute Of Information Technology Allahabad","Indian Institute Of Information Technology Allahabad"),
("INDIAN INSTITUTE OF SCIENCE EDUCATION AND RESEARCH KOLKATA","INDIAN INSTITUTE OF SCIENCE EDUCATION AND RESEARCH KOLKATA"),
("Indian Institute of Space Science and Technology","Indian Institute of Space Science and Technology"),
("Indian Institute of Technology Madras","Indian Institute of Technology Madras"),
("Indian Institute Of Technology, Hyderabad","Indian Institute Of Technology, Hyderabad"),
("Indian School of Mines, Dhanbad","Indian School of Mines, Dhanbad"),
("Indira Gandhi Delhi Technical University for Women, Delhi","Indira Gandhi Delhi Technical University for Women, Delhi"),
("Institute of Technology & Management, Gwalior","Institute of Technology & Management, Gwalior"),
("Institute of Chemical Technology,Mumbai","Institute of Chemical Technology,Mumbai"),
("Institute of Road and transport Technology","Institute of Road and transport Technology"),
("J.B. Institute of Engineering and Technology","J.B. Institute of Engineering and Technology"),
("Jaggaiya peta engineering college","Jaggaiya peta engineering college"),
("Jain college of Engineering (affiliated to VTU)","Jain college of Engineering (affiliated to VTU)"),
("Jamia Milia Islamia, Delhi","Jamia Milia Islamia, Delhi"),
("Jayamukhi Institute Of Technological Sciences","Jayamukhi Institute Of Technological Sciences"),
("Jaypee Insitute of Information Technology,Noida","Jaypee Insitute of Information Technology,Noida"),
("Kakatiya University","Kakatiya University"),
("Krishna Institute of Engineering and Technology","Krishna Institute of Engineering and Technology"),
("Koneru Lakshmaiah University","Koneru Lakshmaiah University"),
("Lourdes Matha College of Science and Technology","Lourdes Matha College of Science and Technology"),
("Madhav Institute of Technology and Science, Gwalior","Madhav Institute of Technology and Science, Gwalior"),
("Maharaja Surajmal Institute of Technology, New Delhi","Maharaja Surajmal Institute of Technology, New Delhi"),
("Manipal Institute of Technology, Manipal","Manipal Institute of Technology, Manipal"),
("Manipal Institute of Technology,Jaipur","Manipal Institute of Technology,Jaipur"),
("Motilal Nehru National Institute of Technology","Motilal Nehru National Institute of Technology"),
("National institute of foundary and forge technology,Ranchi","National institute of foundary and forge technology,Ranchi"),
("National Institute of Technology Agartala","National Institute of Technology Agartala"),
("NATIONAL INSTITUTE OF TECHNOLOGY DURGAPUR","NATIONAL INSTITUTE OF TECHNOLOGY DURGAPUR"),
("National Institute of Technology Karnataka","National Institute of Technology Karnataka"),
("National Institute of Technology Kurukshetra","National Institute of Technology Kurukshetra"),
("National Institute Of technology Meghalaya","National Institute Of technology Meghalaya"),
("National Institute Of Technology Warangal","National Institute Of Technology Warangal"),
("National Institute of Technology, Suratkal","National Institute of Technology, Suratkal"),
("NATIONAL INSTITUTE OF TECHONOLOGY CALICUT","NATIONAL INSTITUTE OF TECHONOLOGY CALICUT"),
("NIT,Jamshedpur","NIT,Jamshedpur"),
("NIT TRICHY","NIT TRICHY"),
("NIT Raipur","NIT Raipur"),
("NIT jalandhar","NIT jalandhar"),
("NBN Sinhgad School of engineering, Ambegaon(Bk), Pune","NBN Sinhgad School of engineering, Ambegaon(Bk), Pune"),
("Osmania university","Osmania university"),
("PES Insitute of Technology,Bangalore","PES Insitute of Technology,Bangalore"),
("Padmabhushan Vasantdada Patil Pratishthan's College of Engineering","Padmabhushan Vasantdada Patil Pratishthan's College of Engineering"),
("Roorkee Institute Of Technology","Roorkee Institute Of Technology"),
("Sanjay Ghodawat Polytechnic Kolhapur","Sanjay Ghodawat Polytechnic Kolhapur"),
("Sardar Vallabhbhai National Institute of Technology","Sardar Vallabhbhai National Institute of Technology"),
("Saurashtra University","Saurashtra University"),
("Savitribai phule pune university","Savitribai phule pune university"),
("Sharda University,Greater Noida","Sharda University,Greater Noida"),
("Shivaji University,Kolhapur","Shivaji University,Kolhapur"),
("Shri Brahmanand Institute of Management and Computer Science","Shri Brahmanand Institute of Management and Computer Science"),
("Shri Govindram Seksaria Institute of Technology and Science","Shri Govindram Seksaria Institute of Technology and Science"),
("Shri Ramdeobaba College of Engineering and Management, Nagpur","Shri Ramdeobaba College of Engineering and Management, Nagpur"),
("SIES GST- Mumbai University","SIES GST- Mumbai University"),
("Sinhgad Institute Of Science and Technology,Narhe","Sinhgad Institute Of Science and Technology,Narhe"),
("Sri Mittapalli College of Engineering","Sri Mittapalli College of Engineering"),
("Sri Ramakrishna Engineering College, Coimbatore","Sri Ramakrishna Engineering College, Coimbatore"),
("Sri Venkateswara university college of engineering","Sri Venkateswara university college of engineering"),
("Stanley college of engineering and technology for women","Stanley college of engineering and technology for women"),
("Swami Keshvanand Institute of Technology Management & Gramothan","Swami Keshvanand Institute of Technology Management & Gramothan"),
("Symbiosis Institute of Computer Studies and Research","Symbiosis Institute of Computer Studies and Research"),
("The LNM Institute of Information Technology","The LNM Institute of Information Technology"),
("TKR College of Engineering Technology","TKR College of Engineering Technology"),
("University of Alabama Huntsville","University of Alabama Huntsville"),
("University Of Calicut","University Of Calicut"),
("University of Delhi","University of Delhi"),
("University of Mumbai","University of Mumbai"),
("University of Pune","University of Pune"),
("University of South Australia","University of South Australia"),
("University of Vigo (Spain)","University of Vigo (Spain)"),
("Uttarakhand Technical University","Uttarakhand Technical University"),
("V R Siddhartha Engineering College","V R Siddhartha Engineering College"),
("V. E. S. Institute of technology","V. E. S. Institute of technology"),
("Vellore instiute of technology","Vellore instiute of technology"),
("Vidya Pratishthan's College of Engineering","Vidya Pratishthan's College of Engineering"),
("Vivekanand Education Society Institute Of Technology","Vivekanand Education Society Institute Of Technology"),
("Walchand College of Engineering","Walchand College of Engineering"))
            

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
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    pin_code = models.IntegerField(default=None)
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
    courses = models.CharField(max_length=32, choices=COURSES)
    year = models.CharField(max_length=32, choices=YEAR)
    university = models.CharField(max_length=100, choices=UNIVERSITY)
    publisher_place = models.CharField(max_length=150)
    isbn = models.CharField(max_length=50)
    edition = models.CharField(max_length=15)
    year_of_pub = models.CharField(max_length=4)
    no_chapters = models.IntegerField(default=0, blank=True)
    contributor = models.ForeignKey(Profile)
    reviewer = models.ForeignKey(Reviewer)
    approved = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    tags = TaggableManager()
    def __unicode__(self):
        name = self.title or 'Book'
        return '%s'%(name)


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

fs = OverwriteStorage(location="/Site/tbc-python_fossee_in/PythonTBC/Python-TBC-Interface/tbc/static/Python-Textbook-Companions/")
        
class Chapters(models.Model):
    name = models.CharField(max_length=200)
    notebook = models.FileField(storage=OverwriteStorage(), upload_to=get_notebook_dir)
    book = models.ForeignKey(Book)
    screen_shots = models.ManyToManyField('ScreenShots')
    def __unicode__(self):
        name = self.name or 'Chapter'
        return '%s'%(name)
    def get_absolute_url(self):
        return sitemap_path+str(self.notebook)


class ScreenShots(models.Model):
    caption = models.CharField(max_length=128)
    image = models.FileField(storage=OverwriteStorage(), upload_to=get_image_dir)
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
    no_chapters = models.IntegerField()
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
    sample_notebook = models.FileField(storage=OverwriteStorage(), upload_to=get_sample_dir)
    def __unicode__(self):
        notebook = self.proposal.accepted.title or 'notebook'
        return '%s'%(notebook)


class ActivityLog(LogEntry):
    proposal_id = models.IntegerField(null=True)
    conversation = models.TextField(null=True)


class AicteBook(models.Model):
    title = models.TextField()
    author = models.CharField(max_length=300)
    category = models.CharField(max_length=32)
    publisher_place = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50)
    edition = models.CharField(max_length=15)
    year_of_pub = models.CharField(max_length=4)
    proposed = models.BooleanField(default=False)
    def __unicode__(self):
        notebook = self.title or 'Book'
        return '%s'%(notebook)
