from django.db import models
from tbc.models import Chapters, Book
from django.contrib.auth.models import User
from django.db.models import Q
import os
import smtplib
from email.mime.text import MIMEText



class Url (models.Model):
    id = models.AutoField(primary_key = True)
    url = models.URLField()
    
    def get_contributor_details(self, counter):
        notebooks = [os.path.join(chapter_name.split("/")[-2], chapter_name.split('/')[-1]) for chapter_name in list(counter.keys())]
        contributor_list  = []
        for notebook,url,number_of_comments in zip(notebooks, list(counter.keys()), list(counter.values())):
            contributor_dict = {}
            contributor_id = Book.objects.filter(Q(chapters__notebook = notebook)).values_list("contributor_id", flat = True)
            contributor = User.objects.filter(id = contributor_id[0]).values("email", "first_name", "last_name")
            contributor_dict ["contributor_email"] = contributor[0]["email"]
            contributor_dict["contributor_name"] = contributor[0]["first_name"]+" "+ contributor[0]["last_name"]
            contributor_dict["url"] = url
            contributor_dict["number_of_comments"] = number_of_comments
            contributor_list.append(contributor_dict)
        return contributor_list
    
    def send_mail_to_contributor(self, contributor_details):
        me  = 'put your localhost mail id'

        for info in contributor_details:
            body = """ Hi {0}, this mail is from TBC-Python Team. You have {1} unread comments for your chapter - {2}""".format(info["contributor_name"],
                                                                                                                                info["number_of_comments"],
                                                                                                                                info["url"]
                                                                                                                                )
            you = info["contributor_email"]

            message = MIMEText(body)
            message["Subject"] = "You have {0} unread comment(s).".format(info["number_of_comments"])
            message ["From"] = me
            message ["To"] = you
            smtp_instance = smtplib.SMTP('localhost')
            smtp_instance.sendmail(me, you, message.as_string())
            smtp_instance.quit()
        return True



class Comments(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    comments = models.TextField()
    is_notified = models.BooleanField(default = False)

