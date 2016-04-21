from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import Url, Comments
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
from collections import Counter
import os.path
from email.mime.text import MIMEText
from django.http import Http404
from tbc.models import Book, Chapters
from tbc.views import is_reviewer

@user_passes_test(lambda u:u.is_superuser, login_url="/admin/login/")

def commenting(request):
    ci = RequestContext(request)
    curr_user = request.user
    if not is_reviewer(curr_user):
        raise Http404("You are not allowed to view this page")
    else:
        url_instance = Url.objects.filter(Q(comments__is_notified = 0)).distinct()
        context = {"url_context": url_instance, "user": curr_user}

        if request.method == "POST":
            notified_comment_list = request.POST.getlist("comment")
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
