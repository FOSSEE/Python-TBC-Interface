import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PythonTBC.settings")
base_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

from commentingapp.models import Url, Comments
from commentingapp.commenting_new import DisqusCommenting
from tbc.models import Book, Chapters
from django.contrib.auth.models import User

class CronForCommenting(object):

    def fetch_comments_from_script(self):
        """ Fetches comment from Commenting script"""

        commenting_instance = DisqusCommenting()
        check_net = commenting_instance.check_internet_connection()
        check_auth = commenting_instance.check_authentication("enter your disqus api public key here", 
                                                               "enter your forum name here"
                                                              ) 
        thread = commenting_instance.get_thread_ids()
        self.comments_for_db = commenting_instance.get_comments()

        return self.comments_for_db



    def add_comments_to_db(self):
    
        if not Url.objects.exists():
            """ Populates the db if empty"""
            for comment_details in self.comments_for_db:
                url_instance =  Url(url = comment_details["chapter_urls"]) #url_instance is actually an object
                url_instance.save()
                for comment in comment_details["comment_list"]:
                    Comments.objects.create(url = url_instance, comments = comment)
            return "Database is created"

        else:
            """ if the db isnt empty"""
            for comment_details in self.comments_for_db:
                url_object, url_status = Url.objects.get_or_create(url = comment_details["chapter_urls"])
                url_primary_key  = url_object.pk
                for comment in comment_details["comment_list"]:
                    Comments.objects.get_or_create(comments = comment, url_id = url_primary_key)
            return "Database is updated."


    def delete_redundant_comments(self):
       	"delete urls that have no comments in them anymore"
        
        url_list = [urls["chapter_urls"] for urls in self.comments_for_db]
        url_list_db = Url.objects.values_list("url", flat = True)
        url_difference = set(url_list_db)-set(url_list)
        for delete_url in url_difference:
            Url.objects.filter(url = delete_url).delete()

        "delete comments that have been deleted from tbc notebooks"
        for comment_details in self.comments_for_db:
            url_instance = Url.objects.get(url = comment_details["chapter_urls"])
            comment_list_db = url_instance.comments_set.values_list("comments", flat = True)
            redundant_comment_list = set(comment_list_db)-set(comment_details["comment_list"])
            for delete_comment in redundant_comment_list:
                url_instance.comments_set.filter(comments = delete_comment).delete()
        return "Redundant Comments deleted."



if __name__ == '__main__':

    a = CronForCommenting()
    b = a.fetch_comments_from_script()
    c = a.add_comments_to_db()        #This should always be before delete_redundant_comments
    d = a.delete_redundant_comments() #This should always be after add_comments_to_db
    print (c)
    print (d)
