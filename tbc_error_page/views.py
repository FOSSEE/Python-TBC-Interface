from django.shortcuts import render_to_response
from .models import Error, Broken, get_json_from_file
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404
from tbc.views import is_reviewer


@login_required(login_url="/login/")
def error(request):
    ci = RequestContext(request)
    curr_user = request.user
    if not is_reviewer(curr_user):
        raise Http404("You are not allowed to view this page")
    else:
        db_instance = Error()
        error_json_data = get_json_from_file("error.pickle")

        if not Error.objects.exists():
            db_instance.create_new_error_data(error_json_data)        
        else:
            db_instance.delete_redundant_error_data(error_json_data)
            db_instance.update_error_data(error_json_data)    

        error_details = Error.objects.filter(is_deliberate = 0)

        if request.method == "POST":
            deliberate_urls_list = request.POST.getlist("deliberate")
            db_instance.update_deliberate_error(deliberate_urls_list)

            context = {"user":request.user, "deliberate" :deliberate_urls_list}
        
            return render_to_response ("deliberate.html", context, ci)


        context = {"context": error_details, "user": curr_user}
        return render_to_response ("error.html", context, ci)

@login_required(login_url="/login/")
def broken(request):
    ci = RequestContext(request)
    curr_user = request.user
    if not is_reviewer(curr_user):
        raise Http404("You are not allowed to view this page")
    else:
        db_instance = Broken()
        broken_json_data = get_json_from_file("broken.pickle")
        
        if not Broken.objects.exists():
            db_instance.create_new_broken_data(broken_json_data)

        else:
            db_instance.delete_redundant_broken_data(broken_json_data)
            db_instance.update_broken_data(broken_json_data)
            
        broken = Broken.objects.all() 
        context = {"broken": broken, "user": curr_user}
        return render_to_response("broken.html", context, ci)


