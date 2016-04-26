from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from .models import Url, Comments
from django.db.models import Q
from collections import Counter
from django.http import Http404
from tbc.models import Book, Chapters
from tbc.views import is_reviewer


@login_required(login_url="/login/")

def commenting(request):
    context = {}
    context.update(csrf(request))
    curr_user = request.user
    if not is_reviewer(curr_user):
        raise Http404("You are not allowed to view this page")
    else:
        url_instance = Url.objects.filter(Q(comments__is_notified = 0)).distinct()
        context["url_context"] = url_instance
        context["reviewer"] =  curr_user

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
                context["notified_comments"] =  "You have suceesfully notified the contributors"
            else:
                context["notified_comments"] = "Mail could not be sent"
            return render_to_response("notified.html", context)


        return render_to_response ("commenting.html", context)
