from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import Url, Comments
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from tbc.models import Book, Chapters
from django.contrib.auth.models import User
from collections import Counter
import os.path
from email.mime.text import MIMEText

@user_passes_test(lambda u:u.is_superuser, login_url="/admin/login/")

def commenting(req):
    ci = RequestContext(req)
    url_instance = Url.objects.filter(Q(comments__is_notified = 0)).distinct()
    context = {"url_context": url_instance, "user": req.user}

    if req.method == "POST":
        notified_comment_list = req.POST.getlist("comment")
        url_list = []
        for notified_comments in notified_comment_list:
            url_comment_list= notified_comments.split(", ")
            url_list.append(url_comment_list[0])
            Comments.objects.filter(comments = url_comment_list[1]).update(is_notified = 1)

        counter  = Counter(url_list)
        url_db_instance = Url()
        contributor_details = url_db_instance.get_contributor_details(counter)
        status = url_db_instance.send_mail_to_contributor(contributor_details)
       
        if status == True:
            context =  {"notified_comments": "You have suceesfully notified the contributors"}
        else:
            context =  {"notified_comments": "Mail couldnot be sent"}
        return render_to_response("notified.html", context, ci)


    return render_to_response ("commenting.html", context, ci)
