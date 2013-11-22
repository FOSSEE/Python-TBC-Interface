from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from models import *
from tbc.forms import *
from local import *
import os
import zipfile
import StringIO
import smtplib
import shutil
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
    books = Book.objects.filter(approved=True)[0:6]
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        curr_user = authenticate(username=username, password=password)
        login(request, curr_user)
        if curr_user.groups.filter(name='reviewer').count() == 1:
            context['reviewer'] = curr_user
            return HttpResponseRedirect("/book-review")
        else:
            context['user'] = curr_user
            try:
                Profile.objects.get(user=curr_user)
                return HttpResponseRedirect("/")
            except:
                return HttpResponseRedirect("/profile")
    else:
        form = UserLoginForm()
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('tbc/login.html', context)


def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
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
        return render_to_response('tbc/profile.html', context)
    else:
        return HttpResponse('invalid user')
        

def UserLogout(request):
    user = request.user
    if user.is_authenticated() and user.is_active:
        logout(request)
    return redirect('/')
    

def SubmitBook(request):
    curr_user = request.user
    context = {}
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            profile = Profile.objects.get(user=request.user.id)
            data.contributor = profile
            data.save()
            context['user'] = curr_user
            return HttpResponseRedirect('/upload-content')
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


def ContentUpload(request):
    user = request.user
    curr_book = Book.objects.order_by("-id")[0]
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
                  "http://dev.fossee.in/book-review/"+str(curr_book.id)
        email_send(book.reviewer.email, subject, message)
        return HttpResponseRedirect('/')
    context = {}
    context.update(csrf(request))
    context['user'] = user
    context['no_notebooks'] = [i for i in range(1, curr_book.no_chapters+1)]
    context['no_images'] = [i for i in range(1, 4)]
    return render_to_response('tbc/upload-content.html', context)


def generateZip(book_id):
    book = Book.objects.get(id=book_id)
    files_to_zip = []
    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = file_path+"/static/uploads/"
    notebooks = Chapters.objects.filter(book=book)
    for notebook in notebooks:
        files_to_zip.append(file_path+str(notebook.notebook))
    zip_subdir = book.title.strip()
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
            books = Book.objects.filter(approved=False)
            context['books'] = books
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/book-review.html', context)
    else:
        return HttpResponse("You are not allowed to view this page.")


def ApproveBook(request, book_id=None):
    user = request.user
    context = {}
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
        "http://dev.fossee.in/internship-forms"+"\n"+\
        "The forms should be duly filled(fill only sections which are applicable) & submit at the following address:\n"+\
        "Dr. Prabhu Ramachandran, \n"+\
        "Department of Aerospace Engineering,\n"+\
        "IIT Bombay, Powai, Mumbai - 400076\n"+\
        "Kindly, write Python Texbook Companion on top of the envelope.\n\n\n"+\
        "Regards,\n"+"Python TBC,\n"+"FOSSEE, IIT - Bombay"
        return HttpResponse(message)
        email_send(book.reviewer.email, subject, message)
        context['user'] = user
        return HttpResponseRedirect("/book-review")
    elif request.method == 'POST' and request.POST['approve_notify'] == "notify":
        return HttpResponseRedirect("/notify-changes/"+book_id)
    else:
        context['user'] = user
        return HttpResponseRedirect("/book-review/"+book_id)
        

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
        else:
            context['book'] = book
            context['book_id'] = book_id
            context['mailto'] = book.contributor.user.email
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/notify-changes.html', context)
    else:
        return HttpResponse('invalid user')


def BrowseBooks(request):
    context = {}
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    images = []
    if request.method == 'POST':
        category = request.POST['category']
        books = Book.objects.filter(category=category)
        for book in books:
            images.append(ScreenShots.objects.filter(book=book)[0])
    else:
        category = 'computer science'
        books = Book.objects.filter(category='computer science')
        for book in books:
            images.append(ScreenShots.objects.filter(book=book)[0])
    context.update(csrf(request))
    book_images = []
    for i in range(len(books)):
        obj = {'book':books[i], 'image':images[i]}
        book_images.append(obj)
    context['items'] = book_images
    context['category'] = category
    return render_to_response('tbc/browse-books.html', context)
