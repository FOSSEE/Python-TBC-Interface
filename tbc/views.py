from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from models import *
from tbc.forms import *
import os
import zipfile
import StringIO
import smtplib
import shutil
import string
import random
from email.mime.text import MIMEText


def email_send(to,subject,msg):
    try:
        smtpObj = smtplib.SMTP('localhost')
        mail_from = "textbook@fosse.in"
        message = MIMEText(msg)
        message['Subject'] = subject
        message['From'] = mail_from
        message['to'] = to
        smtpObj.sendmail(mail_from, to, message.as_string())
    except SMTPException:
        return HttpResponse("Error:unable to send email")


def is_reviewer(user):
    if user.groups.filter(name='reviewer').count() == 1:
        return True


def InternshipForms(request):
    context = {}
    images = []
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    return render_to_response('tbc/internship-forms.html', context)


def AboutPytbc(request):
    context = {}
    images = []
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    return render_to_response('tbc/about-pytbc.html', context)


def Home(request):
    context = {}
    images = []
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    if 'up' in request.GET:
        context['up'] = True
    if 'profile' in request.GET:
        context['profile'] = True
    if 'login' in request.GET:
        context['login'] = True
    if 'logout' in request.GET:
        context['logout'] = True
    if 'update_book' in request.GET:
        context['update_book'] = True
    if 'not_found' in request.GET:
        context['not_found'] = True
    if 'proposal' in request.GET:
        context['proposal_submitted'] = True
    if 'proposal_pending' in request.GET:
        context['proposal_pending'] = True
    books = Book.objects.filter(approved=True).order_by("-id")[0:6]
    for book in books:
        images.append(ScreenShots.objects.filter(book=book)[0])
    context['images'] = images
    book_images = []
    for i in range(len(books)):
        obj = {'book':books[i], 'image':images[i]}
        book_images.append(obj)
    context['items'] = book_images
    return render_to_response('base.html', context)


def UserLogin(request):
    context = {}
    context.update(csrf(request))
    if 'require_login' in request.GET:
        context['require_login'] = True
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if username == "" or password == "":
            form = UserLoginForm()
            context['form'] = form
            context['empty'] = True
            return render_to_response('tbc/login.html', context)
        curr_user = authenticate(username=username, password=password)
        if curr_user is not None:
            login(request, curr_user)
        else:
            form = UserLoginForm()
            context['form'] = form
            context['invalid'] = True
            return render_to_response('tbc/login.html', context)
        if is_reviewer(curr_user):
            context['reviewer'] = curr_user
            return HttpResponseRedirect("/book-review")
        else:
            context['user'] = curr_user
            try:
                Profile.objects.get(user=curr_user)
                return HttpResponseRedirect("/?login=success")
            except:
                return HttpResponseRedirect("/profile/?update=profile")
    else:
        form = UserLoginForm()
        if 'signup' in request.GET:
            context['signup'] = True
    context['form'] = form
    return render_to_response('tbc/login.html', context)


def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/?signup=done')
        else:
            context = {}
            context.update(csrf(request))
            context['form'] = form
            return render_to_response('tbc/register.html', context)
    else:
        form = UserRegisterForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('tbc/register.html', context)


def UserProfile(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return HttpResponseRedirect('/')
            else:
                context = {}
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('tbc/profile.html', context)
        else:
            form = UserProfileForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        context['user'] = user
        if 'update' in request.GET:
            context['profile'] = True
        return render_to_response('tbc/profile.html', context)
    else:
        return HttpResponseRedirect('/login/?require_login=True')


def UserLogout(request):
    user = request.user
    if user.is_authenticated() and user.is_active:
        logout(request)
    return redirect('/?logout=done')


def ForgotPassword(request):
    context = {}
    user_emails = []
    context.update(csrf(request))
    if request.user.is_anonymous():
        context['anonymous'] = True
    if request.method == 'POST':
        email = request.POST['email']
        profiles = Profile.objects.all()
        for profile in profiles:
            user_emails.append(profile.user.email)
        if email in user_emails:
            user = User.objects.get(email=email)
            password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            user.set_password(password)
            user.save()
            subject = "PythonTBC: Password Reset"
            message = "Dear "+user.first_name+",\n"+\
            "Your password for PythonTBC interface has been reset."+\
            "Your credentials are:\n"+\
            "Username: "+user.username+\
            "\nPassword: "+password+\
            "\n\nKindly login with the given password and update your password through the below given link."+\
            "\nLink: http://tbc-python.fossee.in/update-password."+\
            "\n\nThank You !"
            email_send(email, subject, message)
            form = UserLoginForm()
            context['form'] = form
            context['forgot_pass_redirection'] = True
            return render_to_response("tbc/login.html", context)
        else:
            context['invalid_email'] = True
            return render_to_response("tbc/forgot-password.html", context)    
    else:
        return render_to_response("tbc/forgot-password.html", context)


def UpdatePassword(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    if user.is_authenticated():
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm = request.POST['confirm_new_password']
            if new_password == "" or confirm == "":
                form = PasswordResetForm()
                context['empty'] = True
                context['form'] = form
                return render_to_response("tbc/update-password.html", context)
            if new_password == confirm:
                user.set_password(new_password)
                user.save()
                form = UserLoginForm()
                context['password_updated'] = True
                context['form'] = form
                logout(request)
                return render_to_response("tbc/login.html", context)
            else:
                form = PasswordResetForm()
                context['no_match'] = True
                context['form'] = form
                return render_to_response("tbc/update-password.html", context)
        else:
            form = PasswordResetForm()
            context['form'] = form
            return render_to_response("tbc/update-password.html", context)
    else:
        form = UserLoginForm()
        context['form'] = form
        context['require_login'] = True
        return render_to_response("tbc/login.html", context)


def SubmitBook(request):
    curr_user = request.user
    context = {}
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            profile = Profile.objects.get(user=request.user.id)
            data.contributor = profile
            data.reviewer = Reviewer.objects.get(pk=1)
            data.save()
            context['user'] = curr_user
            curr_book = Book.objects.order_by("-id")[0]
            curr_book_id = curr_book.id
            return HttpResponseRedirect('/upload-content/'+str(curr_book_id))
        else:
            context.update(csrf(request))
            context['form'] = form
            context['user'] = curr_user
            return render_to_response('tbc/submit-book.html', context)
    else:
        form = BookForm()
    context.update(csrf(request))
    context['form'] = form
    context['user'] = curr_user
    return render_to_response('tbc/submit-book.html', context)


def SubmitProposal(request):
    curr_user = request.user
    user_profile = Profile.objects.get(user=curr_user.id)
    context = {}
    context.update(csrf(request))
    context['user'] = curr_user
    user_proposals = Proposal.objects.filter(user=user_profile)
    can_submit_new = True
    for proposal in user_proposals:
        if proposal.status is not "book completed":
            can_submit_new = False
    if can_submit_new:
        if request.method == 'POST':
            book_titles = request.POST.getlist('title')
            book_authors = request.POST.getlist('author')
            book_categories = request.POST.getlist('category')
            book_pubs = request.POST.getlist('publisher_place')
            book_isbns = request.POST.getlist('isbn')
            book_editions = request.POST.getlist('edition')
            book_years = request.POST.getlist('year_of_pub')
            book_chapters = request.POST.getlist('no_chapters')
            for item in range(3):
                tempbook = TempBook()
                tempbook.title = book_titles[item]
                tempbook.author = book_authors[item]
                tempbook.category = book_categories[item]
                tempbook.publisher_place = book_pubs[item]
                tempbook.isbn = book_isbns[item]
                tempbook.edition = book_editions[item]
                tempbook.year_of_pub = book_years[item]
                tempbook.no_chapters = book_chapters[item]
                tempbook.save()
            proposal = Proposal()
            proposal.user = user_profile
            proposal.save()
            for book in list(TempBook.objects.all())[-3:]:
                proposal.textbooks.add(book)
            return HttpResponseRedirect('/?proposal=submitted')
        else:
            book_forms = []
            for i in range(3):
                form = BookForm()
                book_forms.append(form)
            context['book_forms'] = book_forms
            return render_to_response('tbc/submit-proposal.html', context)
    else:
        return HttpResponseRedirect('/?proposal_pending=True')


def UpdateBook(request):
    current_user = request.user
    user_profile = Profile.objects.get(user=current_user)
    try:
        book_to_update = Book.objects.get(contributor=user_profile, approved=False) or None
    except:
        return HttpResponseRedirect("/?not_found=True")
    title = book_to_update.title
    chapters = Chapters.objects.filter(book=book_to_update)
    screenshots = ScreenShots.objects.filter(book=book_to_update)
    context = {}
    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book_to_update)
        if book_form.is_valid():
            file_path = os.path.abspath(os.path.dirname(__file__))
            file_path = file_path+"/static/uploads/"
            directory = file_path+book_to_update.contributor.user.first_name
            os.chdir(directory)
            os.popen("mv '"+title+"' '"+book_to_update.title+"'")
            data = book_form.save(commit=False)
            data.contributor = user_profile
            data.save()
            context.update(csrf(request))
            context['form'] = book_form
            return HttpResponseRedirect('/update-content/'+str(book_to_update.id))
    else:
        book_form = BookForm()
        book_form.initial['title'] = book_to_update.title
        book_form.initial['author'] = book_to_update.author
        book_form.initial['publisher_place'] = book_to_update.publisher_place
        book_form.initial['category'] = book_to_update.category
        book_form.initial['isbn'] = book_to_update.isbn
        book_form.initial['edition'] = book_to_update.edition
        book_form.initial['year_of_pub'] = book_to_update.year_of_pub
        book_form.initial['no_chapters'] = book_to_update.no_chapters
        book_form.initial['reviewer'] = book_to_update.reviewer
        context.update(csrf(request))
        context['form'] = book_form
        return render_to_response('tbc/update-book.html', context)


def ContentUpload(request, book_id=None):
    user = request.user
    curr_book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        for i in range(1, curr_book.no_chapters+1):
            chapter = Chapters()
            chapter.name = request.POST['chapter'+str(i)]
            chapter.notebook = request.FILES['notebook'+str(i)]
            chapter.book = curr_book
            chapter.save()
        for i in range(1, 4):
            screenshot = ScreenShots()
            screenshot.caption = request.POST['caption'+str(i)]
            screenshot.image = request.FILES['image'+str(i)]
            screenshot.book = curr_book
            screenshot.save()
        book = Book.objects.order_by("-id")[0]
        subject = "Python-TBC: Book Submission"
        message = "Hi "+curr_book.reviewer.name+",\n"+\
                  "A book has been submitted on the Python TBC interface.\n"+\
                  "Details of the Book & Contributor:\n"+\
                  "Contributor: "+curr_book.contributor.user.first_name+" "+curr_book.contributor.user.last_name+"\n"+\
                  "Book Title: "+curr_book.title+"\n"+\
                  "Author: "+curr_book.author+"\n"+\
                  "Publisher: "+curr_book.publisher_place+"\n"+\
                  "ISBN: "+curr_book.isbn+"\n"+\
                  "Follow the link to review the book: \n"+\
                  "http://tbc-python.fossee.in/book-review/"+str(curr_book.id)
        email_send(book.reviewer.email, subject, message)
        return HttpResponseRedirect('/?up=done')
    context = {}
    context.update(csrf(request))
    context['user'] = user
    context['curr_book'] = curr_book
    context['no_notebooks'] = [i for i in range(1, curr_book.no_chapters+1)]
    context['no_images'] = [i for i in range(1, 4)]
    return render_to_response('tbc/upload-content.html', context)


def UpdateContent(request, book_id=None):
    user = request.user
    current_book = Book.objects.get(id=book_id)
    chapters_to_update = Chapters.objects.filter(book=current_book)
    screenshots_to_update = ScreenShots.objects.filter(book=current_book)
    context = {}
    if request.method == 'POST':
        for i in range(1, current_book.no_chapters+1):
            chapter = Chapters.objects.get(id=chapters_to_update[i-1].id)
            chapter.name = request.POST['chapter'+str(i)]
            chapter.notebook = request.FILES['notebook'+str(i)]
            chapter.book = current_book
            chapter.save()
        for i in range(1, 4):
            screenshot = ScreenShots.objects.get(id=screenshots_to_update[i-1].id)
            screenshot.caption = request.POST['caption'+str(i)]
            screenshot.image = request.FILES['image'+str(i)]
            screenshot.book = current_book
            screenshot.save()
        subject = "Python-TBC: Book Updated"
        message = "Hi "+current_book.reviewer.name+",\n"+\
                  "Submission for a book has been updated on the Python TBC interface.\n"+\
                  "Details of the Book & Contributor:\n"+\
                  "Contributor: "+current_book.contributor.user.first_name+" "+current_book.contributor.user.last_name+"\n"+\
                  "Book Title: "+current_book.title+"\n"+\
                  "Author: "+current_book.author+"\n"+\
                  "Publisher: "+current_book.publisher_place+"\n"+\
                  "ISBN: "+current_book.isbn+"\n"+\
                  "Follow the link to review the book: \n"+\
                  "http://dev.fossee.in/book-review/"+str(current_book.id)
        email_send(current_book.reviewer.email, subject, message)
        return HttpResponseRedirect('/?update_book=done')
    else:
        context.update(csrf(request))
        context['user'] = user
        context['current_book'] = current_book
        context['chapters'] = chapters_to_update
        context['screenshots'] = screenshots_to_update
        return render_to_response('tbc/update-content.html', context)


def generateZip(book_id):
    book = Book.objects.get(id=book_id)
    files_to_zip = []
    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = file_path+"/static/uploads/"
    notebooks = Chapters.objects.filter(book=book)
    for notebook in notebooks:
        files_to_zip.append(file_path+str(notebook.notebook))
    zip_subdir = "PythonTBC"
    zipfile_name = "%s.zip" %zip_subdir
    s = StringIO.StringIO()
    zip_file = zipfile.ZipFile(s, 'w')
    for fpath in files_to_zip:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(book.title, fname)
        zip_file.write(fpath, zip_path)
    zip_file.close()
    return s, zipfile_name


def GetZip(request, book_id=None):
    user = request.user
    s, zipfile_name = generateZip(book_id)
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zipfile_name
    return resp


def BookDetails(request, book_id=None):
    context = {}
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    book = Book.objects.get(id=book_id)
    chapters = Chapters.objects.filter(book=book)
    images = ScreenShots.objects.filter(book=book)
    context['chapters'] = chapters
    context['images'] = images
    context['book'] = book
    return render_to_response('tbc/book-details.html', context)


def BookReview(request, book_id=None):
    context = {}
    if is_reviewer(request.user):
        if book_id:
            book = Book.objects.get(id=book_id)
            chapters = Chapters.objects.filter(book=book)
            images = ScreenShots.objects.filter(book=book)
            context['chapters'] = chapters
            context['images'] = images
            context['book'] = book
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/book-review-details.html', context)
        else:
            if 'book_review' in request.GET:
                context['book_review'] = True
            if 'mail_notify' in request.GET:
                context['mail_notify'] = True
            books = Book.objects.filter(approved=False)
            context['books'] = books
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/book-review.html', context)
    else:
        return render_to_response('tbc/forbidden.html')


def ApproveBook(request, book_id=None):
    user = request.user
    context = {}
    if is_reviewer(request.user):
        if request.method == 'POST' and request.POST['approve_notify'] == "approve":
            book = Book.objects.get(id=book_id)
            book.approved = True
            book.save()
            file_path = os.path.abspath(os.path.dirname(__file__))
            zip_path = "/".join(file_path.split("/")[1:-2])
            zip_path = "/"+zip_path+"/Python-Textbook-Companions/"
            file_path = file_path+"/static/uploads/"
            directory = file_path+book.contributor.user.first_name
            os.chmod(directory, 0777)
            os.chdir(directory)
            fp = open(book.title+"/README.txt", 'w')
            fp.write("Contributed By: "+book.contributor.user.first_name+" "+book.contributor.user.last_name+"\n")
            fp.write("Course: "+book.contributor.course+"\n")
            fp.write("College/Institute/Organization: "+book.contributor.insti_org+"\n")
            fp.write("Department/Designation: "+book.contributor.dept_desg+"\n")
            fp.write("Book Title: "+book.title+"\n")
            fp.write("Author: "+book.author+"\n")
            fp.write("Publisher: "+book.publisher_place+"\n")
            fp.write("Year of publication: "+book.year_of_pub+"\n")
            fp.write("Isbn: "+book.isbn+"\n")
            fp.write("Edition: "+book.edition)
            fp.close()
            x = shutil.copytree(book.title, zip_path+book.title)
            subject = "Python-TBC: Book Completion"
            message = "Hi "+book.contributor.user.first_name+",\n"+\
            "Congratulations !\n"+\
            "The book - "+book.title+" is now complete.\n"+\
            "Please visit the below given link to download the forms to be filled to complete the formalities.\n"+\
            "http://tbc-python.fossee.in/internship-forms"+"\n"+\
            "The forms should be duly filled(fill only sections which are applicable) & submit at the following address:\n"+\
            "Dr. Prabhu Ramachandran, \n"+\
            "Department of Aerospace Engineering,\n"+\
            "IIT Bombay, Powai, Mumbai - 400076\n"+\
            "Kindly, write Python Texbook Companion on top of the envelope.\n\n\n"+\
            "Regards,\n"+"Python TBC,\n"+"FOSSEE, IIT - Bombay"
            email_send(book.reviewer.email, subject, message)
            context['user'] = user
            return HttpResponseRedirect("/book-review/?book_review=done")
        elif request.method == 'POST' and request.POST['approve_notify'] == "notify":
            return HttpResponseRedirect("/notify-changes/"+book_id)
        else:
            context['user'] = user
            return HttpResponseRedirect("/book-review/"+book_id)
    else:
        return render_to_response('tbc/forbidden.html')


def NotifyChanges(request, book_id=None):
    context = {}
    if is_reviewer(request.user):
        book = Book.objects.get(id=book_id)
        if request.method == 'POST':
            changes_required = request.POST['changes_required']
            subject = "Python-TBC: Corrections Required"
            message = "Hi, "+book.contributor.user.first_name+",\n"+\
            "Book titled, "+book.title+" requires following changes: \n"+\
            changes_required
            context.update(csrf(request))
            email_send(book.contributor.user.email, subject, message)
            return HttpResponseRedirect("/book-review/?mail_notify=done")
        else:
            context['book'] = book
            context['book_id'] = book_id
            context['mailto'] = book.contributor.user.email
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/notify-changes.html', context)
    else:
        return render_to_response('tbc/forbidden.html')


def BrowseBooks(request):
    context = {}
    category = None
    images = []
    book_images = []
    books = None
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    context.update(csrf(request))
    books = Book.objects.filter(approved=True)
    if request.method == "POST":
        category = request.POST['category']
        if category == "all":
            books = Book.objects.filter(approved=True)
        else:
            books = Book.objects.filter(category=category, approved=True)
    else:
        books = Book.objects.filter(approved=True)
    for book in books:
       images.append(ScreenShots.objects.filter(book=book)[0])
    for i in range(len(books)):
       obj = {'book':books[i], 'image':images[i]}
       book_images.append(obj)
    context['items'] = book_images
    context['category'] = category
    return render_to_response('tbc/browse-books.html', context)


def ConvertNotebook(request, notebook_path=None):
    path = os.path.abspath(os.path.dirname(__file__))
    path = path+"/static/uploads/"
    path = path+notebook_path
    notebook_name = path.split("/")[-1:]
    notebook_name = notebook_name[0].split(".")[0]
    path = path.split("/")[0:-1]
    path = "/".join(path)+"/"
    os.chdir(path)
    try:
        template = path.split("/")[8:]
        template = "/".join(template)+notebook_name+".html"
        return render_to_response(template, {})
    except:
        os.popen("ipython nbconvert --to html \""+path+notebook_name+".ipynb\"")
        template = path.split("/")[8:]
        template = "/".join(template)+notebook_name+".html"
        return render_to_response(template, {})
