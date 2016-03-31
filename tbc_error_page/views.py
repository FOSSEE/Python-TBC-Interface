from django.shortcuts import render_to_response
from .models import Error, Broken, get_json_from_file
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
import json
import os


#@login_required(login_url="/admin/login/")
@user_passes_test(lambda u:u.is_superuser, login_url="/admin/login")



def error(req):
    ci = RequestContext(req)
    db_instance = Error()
    error_json_data = get_json_from_file("error.json")

    if not Error.objects.exists():
        db_instance.create_new_error_data(error_json_data)        
    else:
        db_instance.delete_redundant_error_data(error_json_data)
        db_instance.update_error_data(error_json_data)    

    error_details = Error.objects.filter(is_deliberate = 0)

    if req.method == "POST":
        deliberate_urls_list = req.POST.getlist("deliberate")
        db_instance.update_deliberate_error(deliberate_urls_list)

        context = {"user":req.user, "deliberate" :deliberate_urls_list}
    
        return render_to_response ("deliberate.html", context, ci)


    context = {"context": error_details, "user": req.user}
    return render_to_response ("error.html", context, ci)

def broken(req):

    ci = RequestContext(req)    
    db_instance = Broken()
    broken_json_data = get_json_from_file("broken.json")
    
    if not Broken.objects.exists():
        db_instance.create_new_broken_data(broken_json_data)

    else:
        db_instance.delete_redundant_broken_data(broken_json_data)
        db_instance.update_broken_data(broken_json_data)
        
    broken = Broken.objects.all() 
    context = {"broken": broken, "user": req.user}
    return render_to_response("broken.html", context, ci)


