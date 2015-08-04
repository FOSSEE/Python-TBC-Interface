from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.models import CHANGE
from django.contrib.auth.decorators import login_required
from models import *
from tbc.forms import *
import local
import os
import zipfile
import StringIO
import smtplib
import shutil
import string
import random
import json
import subprocess
from email.mime.text import MIMEText


def add_log(user, object, flag, message, proposal_id=None, chat='No message'):
    '''Creates log entry of the user activities.'''
    ActivityLog(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(object).id,
        object_id=object.id,
        object_repr=force_text(object),
        action_flag=flag,
        change_message=message,
        proposal_id = proposal_id,
        conversation = chat,
    ).save()


def email_send(to,subject,msg):
    try:
        smtpObj = smtplib.SMTP('localhost')
        mail_from = "textbook@fossee.in"
        message = MIMEText(msg)
        message['Subject'] = subject
        message['From'] = mail_from
        message['to'] = to
        smtpObj.sendmail(mail_from, to, message.as_string())
    except SMTPException:
        return HttpResponse("Error:unable to send email")


def is_reviewer(user):
    if user.groups.filter(name='reviewer').exists():
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


def SampleIpynb(request):
    return render_to_response('tbc/sample.html')


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
    if 'book_pending' in request.GET:
        context['book_pending'] = True
    if 'no_book_alloted' in request.GET:
        context['no_book_alloted'] = True
    if 'sample_notebook' in request.GET:
        context['sample_notebook'] = True
    if 'cannot_submit_sample' in request.GET:
        context['cannot_submit_sample'] =True
    if 'bookupdate' in request.GET:
        context['bookupdate'] =True

    books = Book.objects.filter(approved=True).order_by("-id")[0:6]
    for book in books:
        try:
            images.append(ScreenShots.objects.filter(book=book)[0])
        except:
            return HttpResponse(book)
    context['images'] = images
    book_images = []
    for i in range(len(books)):
        obj = {'book':books[i], 'image':images[i]}
        book_images.append(obj)
    context['items'] = book_images

    #Check if user is logged in and fetch user's pending proposal ID
    if context.get('user'):
        curr_user = request.user
        user_profile = Profile.objects.filter(user=curr_user)

        pending_proposal_list = list(Proposal.objects.filter(status="pending").order_by('id'))
        try:
            pending_user_proposal = Proposal.objects.get(user=user_profile, status="pending")
        except:
            pending_user_proposal = None

        if pending_user_proposal:
            context['proposal_position'] = pending_proposal_list.index(pending_user_proposal) + 1

    return render_to_response('base.html', context)


def _checkProfile(user):
    return Profile.objects.filter(user=user).exists()


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
            add_log(curr_user, curr_user, CHANGE, 'Logged in')
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
    context = {}
    context.update(csrf(request))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            check_email = User.objects.filter(email=email)
            if check_email:
                context['form'] = form
                context['DuplicateEmail'] = True
                return render_to_response('tbc/register.html', context)
            else:
                user = form.save()
                add_log(user, user, CHANGE, 'Registered')
                return HttpResponseRedirect('/login/?signup=done')
        else:
            context = {}
            context.update(csrf(request))
            context['form'] = form
            return render_to_response('tbc/register.html', context)
    else:
        form = UserRegisterForm()
    context['form'] = form
    return render_to_response('tbc/register.html', context)


def UserProfile(request):
    context = {}
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            user_profile = Profile.objects.filter(user=user)
            if user_profile.exists():
                form = UserProfileForm(request.POST, instance=user_profile[0])
            else:
                form = UserProfileForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                add_log(user, user, CHANGE,'Profile entry')
                return HttpResponseRedirect('/')
            else:
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('tbc/profile.html', context)
        else:
            form = UserProfileForm()
        context.update(csrf(request))
        context['form'] = form
        context['user'] = user
        if 'update' in request.GET:
            context['profile'] = True
        return render_to_response('tbc/profile.html', context)
    else:
        return HttpResponseRedirect('/login/?require_login=True')


def UpdateProfile(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    if user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    if not _checkProfile(user):
        return HttpResponseRedirect("/profile/?update=profile")
    context['user'] = user   
    user_profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            add_log(user, user, CHANGE,'Profile entry')
            return HttpResponseRedirect('/')
        else:
            context['form'] = form
            return render_to_response('tbc/update-profile.html', context)
    else:
        form = UserProfileForm()
        form.initial['about'] = user_profile.about
        form.initial['insti_org'] = user_profile.insti_org
        form.initial['course'] = user_profile.course
        form.initial['dept_desg'] = user_profile.dept_desg
        form.initial['dob'] = user_profile.dob
        form.initial['gender'] = user_profile.gender
        form.initial['phone_no'] = user_profile.phone_no
        form.initial['about_proj'] = user_profile.about_proj
    context['form'] = form
    return render_to_response('tbc/update-profile.html', context)

def UserLogout(request):
    user = request.user
    if user.is_authenticated() and user.is_active:
        logout(request)
    add_log(user, user, CHANGE, 'Logged out')
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
            message = """Dear """+user.first_name+""",\nYour password for Python TBC interface has been reset. Your credentials are:\nUsername: """+user.username+"""\nPassword: """+password+"""\n\nKindly login with the given password and update your password through the link given below.\nLink: http://tbc-python.fossee.in/update-password.\n\nThank You !\n\nRegards,\n Python TBC Team,\nFOSSEE - IIT Bombay."""
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
    context = {}
    user = request.user
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
                add_log(user, user, CHANGE, 'Password updated')
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
    context = {}
    if request.user.is_anonymous():
        return HttpResponseRedirect("/login/?require_login=true")
    else:
        curr_user = request.user
        if curr_user.is_authenticated():
            if not _checkProfile(curr_user):
                return HttpResponseRedirect("/profile/?update=profile")
    user_profile = Profile.objects.get(user=curr_user)
    curr_proposals = Proposal.objects.filter(user=user_profile)
    user_books = Book.objects.filter(contributor=user_profile)
    can_submit_book = True
    for proposal in curr_proposals:
        if proposal.status not in ['book completed', 'rejected']:
            can_submit_book = False
    for book in user_books:
        if not book.approved:
            can_submit_book = False
    if can_submit_book:
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                profile = Profile.objects.get(user=request.user.id)
                data.contributor = profile
                data.reviewer = Reviewer.objects.get(pk=2)
                data.save()
                context['user'] = curr_user
                curr_book = Book.objects.order_by("-id")[0]
                curr_book_id = curr_book.id
                return HttpResponseRedirect('/submit-code-old/'+str(curr_book_id))
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
    else:
        return HttpResponseRedirect('/?book_pending=True')
        


def SubmitCodeOld(request, book_id=None):
    user = request.user
    if not _checkProfile(user):
        return HttpResponseRedirect("/profile/?update=profile")
    curr_profile = Profile.objects.get(user=user)
    context = {}
    dict = {}
    curr_book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        for i in range(1, curr_book.no_chapters+1):
            chapter = Chapters()
            chapter.name = request.POST['chapter'+str(i)]
            dict['chapter'+str(i)] = chapter.name
            chapter.notebook = request.FILES['notebook'+str(i)]
            chapter.book = curr_book
            chapter.save()
        for i in range(1, 4):
            screenshot = ScreenShots()
            screenshot.caption = request.POST['caption'+str(i)]
            screenshot.image = request.FILES['image'+str(i)]
            screenshot.book = curr_book
            screenshot.save()
            chapter_image = request.POST['chapter_image'+str(i)]
            chapter = list(Chapters.objects.filter(name=dict[chapter_image]))[-1]
            chapter.screen_shots.add(screenshot)
            chapter.save()
        subject = "Python-TBC: Codes Submitted Acknowledgement"
        message = """Hi """+curr_book.contributor.user.first_name+""",\nThank you for your contribution to Python TBC.\nWe have received the book & codes submitted by you.\nDetails of the book are given below: \nBook Title: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\n\nPlease be patient while we review your book & get back to you. Review of the book will take a minimum of 25 days. Hoping for kind cooperation."""
        email_send(curr_book.contributor.user.email, subject, message)
        subject = "Python-TBC: Book Submission"
        message = """Hi """+curr_book.reviewer.name+""",\nA book has been submitted on the Python TBC interface.\n Details of the book & contributor:\n Contributor: """+curr_book.contributor.user.first_name+""" """+curr_book.contributor.user.last_name+"""\nBook Title"""+curr_book.title+"""\nAuthor: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\nFollow the link to riview the book:\nhttp://tbc-python.fosse.in/book-review/"""+str(curr_book.id)
        email_send(curr_book.reviewer.email, subject, message)
        return HttpResponseRedirect('/?up=done')
    else:
        context.update(csrf(request))
        context['user'] = user
        context['curr_book'] = curr_book
        context['no_notebooks'] = [i for i in range(1, curr_book.no_chapters+1)]
        context['no_images'] = [i for i in range(1, 4)]
        return render_to_response('tbc/upload-content-old.html', context)


def SubmitProposal(request):
    curr_user = request.user
    if not _checkProfile(curr_user):
        return HttpResponseRedirect("/profile/?update=profile")
    user_profile = Profile.objects.get(user=curr_user.id)
    context = {}
    context.update(csrf(request))
    context['user'] = curr_user
    user_proposals = list(Proposal.objects.filter(user=user_profile))
    proposal_id = None
    can_submit_new = True
    matching_books = []
    for proposal in user_proposals:
        if proposal.status != 'book completed':
            can_submit_new = False
        if proposal.status == 'rejected':
            can_submit_new = True
            proposal_id = proposal.id

    if can_submit_new:
        if request.method == 'POST':
            try:
                proposal = Proposal.objects.get(id=proposal_id)
            except:
                proposal = Proposal()
            proposal.user = user_profile
            proposal.status = 'Pending'
            proposal.save()
            book_titles = request.POST.getlist('title')
            book_authors = request.POST.getlist('author')
            book_categories = request.POST.getlist('category')
            book_pubs = request.POST.getlist('publisher_place')
            book_isbns = request.POST.getlist('isbn')
            book_editions = request.POST.getlist('edition')
            book_years = request.POST.getlist('year_of_pub')
            book_chapters = request.POST.getlist('no_chapters')
            textbooks = proposal.textbooks.all()
            textbooks.delete()
            proposed_books = []
            for item in range(3):
                tempbook = TempBook(no_chapters=0)
                tempbook.title = book_titles[item]
                tempbook.author = book_authors[item]
                tempbook.category = book_categories[item]
                tempbook.publisher_place = book_pubs[item]
                tempbook.isbn = book_isbns[item]
                tempbook.edition = book_editions[item]
                tempbook.year_of_pub = book_years[item]
                tempbook.save()
                proposal.textbooks.add(tempbook)
                proposed_books.append(tempbook)
            subject = "Python TBC: Proposal Acknowledgement"
            message = """Dear """+proposal.user.user.first_name+""",\n
Thank you for showing interest in contributing to Python Textbook Companion Activity.\n\nWe have received your proposal. Details of the books proposed by you are given below:\n\nBook Preference 1\nTitle: """+proposed_books[0].title+"""\nAuthor: """+proposed_books[0].author+"""\nEdition: """+proposed_books[0].edition+"""\nISBN: """+proposed_books[0].isbn+"""\nPublisher: """+proposed_books[0].publisher_place+"""\nYear of Publication: """+proposed_books[0].year_of_pub+"""\n\nBook Preference 2\nTitle: """+proposed_books[1].title+"""\nAuthor: """+proposed_books[1].author+"""\nEdition: """+proposed_books[1].edition+"""\nISBN: """+proposed_books[1].isbn+"""\nPublisher: """+proposed_books[1].publisher_place+"""\nYear of Publication: """+proposed_books[1].year_of_pub+"""\n\nBook Preference 3\nTitle: """+proposed_books[2].title+"""\nAuthor: """+proposed_books[2].author+"""\nEdition: """+proposed_books[2].edition+"""\nISBN: """+proposed_books[2].isbn+"""\nPublisher: """+proposed_books[2].publisher_place+"""\nYear of Publication: """+proposed_books[2].year_of_pub+"""\n\nPlese be patient while we review your proposal. You will be notified to submit sample notebook once the proposal hase been reviewed.\n\nRegards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
            add_log(curr_user, proposal, CHANGE, 'Proposed Books', proposal.id)
            email_send(proposal.user.user.email, subject, message)
            return HttpResponseRedirect('/?proposal=submitted')
        else:
            book_forms = []
            for i in range(3):
                form = BookForm()
                if proposal_id:
                    proposal = Proposal.objects.get(id=proposal_id)
                    textbooks = proposal.textbooks.all()
                    if len(textbooks) == 3:
                        form.initial['title'] = textbooks[i].title
                        form.initial['author'] = textbooks[i].author
                        form.initial['category'] = textbooks[i].category
                        form.initial['publisher_place'] = textbooks[i].publisher_place
                        form.initial['isbn'] = textbooks[i].isbn
                        form.initial['edition'] = textbooks[i].edition
                        form.initial['year_of_pub'] = textbooks[i].year_of_pub
                        form.initial['no_chapters'] = textbooks[i].no_chapters

                book_forms.append(form)
            context['book_forms'] = book_forms
            return render_to_response('tbc/submit-proposal.html', context)
    else:
        return HttpResponseRedirect('/?proposal_pending=True')


def ListAICTE(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        curr_user = request.user
    if not _checkProfile(curr_user):
        return HttpResponseRedirect("/profile/?update=profile")
    user_profile = Profile.objects.get(user=curr_user.id)
    user_proposals = Proposal.objects.filter(user=user_profile)
    context = {}
    context.update(csrf(request))
    context['user'] = curr_user
    if request.method == "POST":
        category = request.POST['category']
        return HttpResponse(category)
        context['category'] = category
        if category == "all":
            aicte_books = AicteBook.objects.filter(proposed=0)
        else:
            aicte_books = AicteBook.objects.filter(category=category, proposed=0)
        if len(aicte_books) == 0:
            context['no_books'] = True
    else:
        aicte_books = AicteBook.objects.filter(proposed=0)
        context['aicte_books'] = aicte_books
    return render_to_response('tbc/aicte-books.html', context)


def SubmitAICTEProposal(request, aicte_book_id=None):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        curr_user = request.user
    if not _checkProfile(curr_user):
        return HttpResponseRedirect("/profile/?update=profile")
    user_profile = Profile.objects.get(user=curr_user.id)
    context = {}
    context.update(csrf(request))
    context['user'] = curr_user
    user_proposals = Proposal.objects.filter(user=user_profile)
    book_proposed = AicteBook.objects.get(id=aicte_book_id)
    context['aicte_book'] = book_proposed
    can_submit_new = True
    proposal_id = None
    for proposal in user_proposals:
        if proposal.status != "book completed":
            can_submit_new = False
        if proposal.status == 'rejected':
            can_submit_new = True
            proposal_id = proposal.id
    if can_submit_new:
        if request.method == 'POST':
            book_proposed.title = request.POST['title']
            book_proposed.author = request.POST['author']
            book_proposed.category = request.POST['category']
            book_proposed.publisher_place = request.POST['publisher_place']
            book_proposed.isbn = request.POST['isbn']
            book_proposed.edition = request.POST['edition']
            book_proposed.year_of_pub = request.POST['year_of_pub']
            book_proposed.proposed = True
            book_proposed.save()
            try:
                proposal = Proposal.objects.get(id=proposal_id)
            except:
                proposal = Proposal()
            proposal.user = user_profile
            proposal.status = 'Pending'
            proposal.save()
            textbooks = proposal.textbooks.all()
            if textbooks:
                textbooks.delete()
            tempbook = TempBook(no_chapters=0)
            tempbook.title = book_proposed.title
            tempbook.author = book_proposed.author
            tempbook.category = book_proposed.category
            tempbook.publisher_place = book_proposed.publisher_place
            tempbook.isbn = book_proposed.isbn
            tempbook.edition = book_proposed.edition
            tempbook.year_of_pub = book_proposed.year_of_pub
            tempbook.save()
            proposal.textbooks.add(tempbook)
            add_log(curr_user, proposal, CHANGE, 'AICTE proposal' ,proposal.id)
            subject = "Python TBC: Proposal Acknowledgement"
            message = """Dear """+proposal.user.user.first_name+""",\n
Thank you for showing interest in contributing to Python Textbook Companion Activity.\n\nWe have received your proposal & you have chosen to contribute an AICTE recommended book. Detail of the book you proposed is given below:\nTitle: """+tempbook.title+"""\nAuthor: """+tempbook.author+"""\nEdition: """+tempbook.edition+"""\nISBN: """+tempbook.isbn+"""\nPublisher: """+tempbook.publisher_place+"""\nYear of Publication: """+tempbook.year_of_pub+"""\n\nRegards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
            email_send(proposal.user.user.email, subject, message)
            return HttpResponseRedirect('/?proposal=submitted')
        else:
            book_form = BookForm()
            book_form.initial['title'] = book_proposed.title
            book_form.initial['author'] = book_proposed.author
            book_form.initial['publisher_place'] = book_proposed.publisher_place
            book_form.initial['category'] = book_proposed.category
            book_form.initial['isbn'] = book_proposed.isbn
            book_form.initial['edition'] = book_proposed.edition
            book_form.initial['year_of_pub'] = book_proposed.year_of_pub
            context['form'] = book_form
            return render_to_response('tbc/confirm-aicte-details.html', context)
    else:
        return HttpResponseRedirect('/?proposal_pending=True')


def ReviewProposals(request, proposal_id=None, textbook_id=None):
    context = {}
    user = request.user
    if is_reviewer(user):
        context['reviewer'] = user
        if proposal_id:
            proposal = Proposal.objects.get(id=proposal_id)
            accepted_book = TempBook.objects.get(id=textbook_id)
            new_book = Book()
            new_book.title = accepted_book.title
            new_book.author = accepted_book.author
            new_book.category = accepted_book.category
            new_book.publisher_place = accepted_book.publisher_place
            new_book.isbn = accepted_book.isbn
            new_book.edition = accepted_book.edition
            new_book.year_of_pub = accepted_book.year_of_pub
            new_book.no_chapters = accepted_book.no_chapters
            new_book.contributor = proposal.user
            new_book.reviewer = Reviewer.objects.get(pk=2)
            new_book.save()
            proposal.status = "samples"
            proposal.accepted = new_book
            proposal.save()
            add_log(user, proposal, CHANGE, 'Proposal accepted', proposal.id)
            subject = "Python-TBC: Proposal Reviewed"
            message = """Dear """+proposal.user.user.first_name+""", \n\nYour recent proposal for Python TBC has been reviewed and the book titled """+proposal.accepted.title+""" by """+proposal.accepted.author+""" has been approved. You may now submit the sample notebook on the interface. Once the sample notebook is approved, the book will be alloted to you.\n\nRegards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
            email_send(proposal.user.user.email, subject, message)
            return HttpResponseRedirect("/proposal-review")
        else:
            new_proposals = Proposal.objects.filter(status="pending").order_by('id')
            old_proposals = []
            old_proposal_status = ['samples', 'sample disapproved', 'sample resubmitted', 'sample submitted']
            proposals = Proposal.objects.filter(status__in=old_proposal_status)
            for proposal in proposals:
                try:
                    sample_notebook = SampleNotebook.objects.get(proposal=proposal)
                except:
                    sample_notebook = None
                obj = {'proposal':proposal, 'sample':sample_notebook}
                old_proposals.append(obj)
            if new_proposals.count() > 0:
                no_new_proposal = False
            else:
                no_new_proposal = True
            context['no_new_proposal'] = no_new_proposal
            context['proposals'] = new_proposals
            context['old_proposals'] = old_proposals
            return render_to_response('tbc/review-proposal.html', context)
    else:
        return HttpResponse("not allowed")


def DisapproveProposal(request, proposal_id=None):
    context = {}
    context.update(csrf(request))
    proposal = Proposal.objects.get(id=proposal_id)
    if request.method == 'POST':
        changes_required = request.POST['changes_required']
        subject = "Python-TBC: Corrections Required in the sample notebook"
        message = """Hi, """+proposal.user.user.first_name+""",\nSample notebook submitted by you for the book titled, """+proposal.accepted.title+""",\nrequires following changes: \n"""+changes_required+"""\n\nKindly make the necessary changes and upload the sample notebook again.\n\nThank You !\n\n Regards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
        add_log(request.user, proposal, CHANGE, 'Sample disapproved',
                proposal_id, chat=subject + '\n' + changes_required)
        context.update(csrf(request))
        proposal.status = "sample disapproved"
        proposal.save()
        email_send(proposal.user.user.email, subject, message)
        return HttpResponseRedirect("/book-review/?mail_notify=done")
    else:
        context['proposal'] = proposal
        return render_to_response('tbc/disapprove-sample.html', context)


def AllotBook(request, proposal_id=None):
    context = {}
    proposal = Proposal.objects.get(id=proposal_id)
    proposal.status = "book alloted"
    proposal.save()
    subject = "Python-TBC: Book Alloted"
    message = """Hi """+proposal.user.user.first_name+""",\n The sample examples for the book '"""+proposal.accepted.title+"""' are correct. Hence, the book is now allotted to you. A time period of 2 months from today is allotted to you for completion of the book. Convert all the solved/worked examples of all the chapters. You can get back to us for any queries.\n\nGood Luck!\n\nRegards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
    add_log(request.user, proposal, CHANGE, 'Book alloted', proposal_id)
    email_send(proposal.user.user.email, subject, message)
    return HttpResponseRedirect("/book-review/?book_alloted=done")


def RejectProposal(request, proposal_id=None):
    context = {}
    context.update(csrf(request))
    proposal = Proposal.objects.get(id=proposal_id)
    if request.method == 'POST':
        books = proposal.textbooks.all() 
        if len(books) == 1:
            aicte_book = AicteBook.objects.get(isbn=books[0].isbn)
            aicte_book.proposed = False
            aicte_book.save()
        proposal.status = 'rejected'
        proposal.save()
        remarks = request.POST['remarks']
        subject = "Python-TBC: Rejection of Proposal"
        message = """Dear """+proposal.user.user.first_name+"""\nYour recent proposal for contributing in Python TBC has been rejected for the following reasons\n"""+request.POST.get('remarks')+"""\n\nHowever, your last proposal will be saved and you can edit the same proposal or propose a fresh one again.\n\nRegards\nPython TBC Team\nFOSSEE - IIT Bombay"""
        add_log(request.user, proposal, CHANGE, 'Proposal rejected',
                proposal.id, chat=subject + '\n' + remarks)
        email_send(proposal.user.user.email, subject, message)
        context.update(csrf(request))
        return HttpResponseRedirect("/book-review/?reject-proposal=done")
    else:
        context['proposal'] = proposal
        return render_to_response('tbc/reject-proposal.html', context)


def SubmitSample(request, proposal_id=None, old_notebook_id=None):
    context = {}
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        user = request.user
    if not _checkProfile(user):
        return HttpResponseRedirect("/profile/?update=profile")
    context.update(csrf(request))
    if request.method == "POST":
        curr_proposal = Proposal.objects.get(id=proposal_id)
        add_log(user, curr_proposal, CHANGE, 'Sample Submitted', curr_proposal.id)
        if old_notebook_id:
            old_notebook = SampleNotebook.objects.get(id=old_notebook_id)
            old_notebook.proposal = curr_proposal
            old_notebook.name = request.POST.get('ch_name_old')
            old_notebook.sample_notebook = request.FILES['old_notebook']
            old_notebook.save()
            curr_proposal.status = "sample resubmitted"
            curr_proposal.save()
            return HttpResponseRedirect('/?sample_notebook=done')
        else:
            sample_notebook = SampleNotebook()
            sample_notebook.proposal = curr_proposal
            sample_notebook.name = request.POST.get('ch_name')
            sample_notebook.sample_notebook = request.FILES['sample_notebook']
            sample_notebook.save()
            curr_proposal.status = "sample submitted"
            curr_proposal.save()
            return HttpResponseRedirect('/?sample_notebook=done')
    else:
        profile = Profile.objects.get(user=user)
        try:
            proposal = Proposal.objects.get(user=profile, status__in=['samples','sample disapproved'])
        except Proposal.DoesNotExist:
            return HttpResponseRedirect('/?cannot_submit_sample=True')
        try:
            old_notebook = SampleNotebook.objects.get(proposal=proposal)
            context['has_old'] = True
            context['old_notebook'] = old_notebook
            context['proposal'] = proposal
            return render_to_response('tbc/submit-sample.html', context)
        except:
            context['proposal'] = proposal
            return render_to_response('tbc/submit-sample.html', context)


def ConfirmBookDetails(request):
    context = {}
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        current_user = request.user
    if not _checkProfile(current_user):
        return HttpResponseRedirect("/profile/?update=profile")
    user_profile = Profile.objects.get(user=current_user)
    try:
        proposal = Proposal.objects.get(user=user_profile, status__in=["book alloted", "codes disapproved"])
    except:
        return HttpResponseRedirect('/?no_book_alloted=true')
    book_to_update = Book.objects.get(id=proposal.accepted.id)
    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book_to_update)
        if book_form.is_valid():
            data = book_form.save(commit=False)
            data.contributor = user_profile
            data.save()
            context.update(csrf(request))
            context['form'] = book_form
            add_log(current_user, book_to_update, CHANGE, 'Book updated', proposal.id)
            if proposal.status == "codes disapproved":
                chapters = Chapters.objects.filter(book=book_to_update)
                screen_shots = ScreenShots.objects.filter(book=book_to_update)
                context.update(csrf(request))
                context['book'] = book_to_update
                context['chapters'] = chapters
                context['screenshots'] = screen_shots
                context['no_notebooks'] = [i for i in range(1, book_to_update.no_chapters+1)]
                return render_to_response('tbc/update-code.html', context)
            return HttpResponseRedirect('/submit-code/')
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
        context['book'] = book_to_update
        return render_to_response('tbc/confirm-details.html', context)


def SubmitCode(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        user = request.user
    if not _checkProfile(user):
        return HttpResponseRedirect("/profile/?update=profile")
    curr_profile = Profile.objects.get(user=user)
    context = {}
    try:
        curr_proposal = Proposal.objects.get(user=curr_profile, status__in=['book alloted', 'codes disapproved'])
        curr_book = curr_proposal.accepted
    except:
        return HttpResponseRedirect('/?no_book_alloted=true')
    dict = {}
    if curr_proposal.status == "codes disapproved":
        if request.method == 'POST':
            chapters = Chapters.objects.filter(book=curr_book)
            old_chapter_count = len(chapters)
            screen_shots = ScreenShots.objects.filter(book=curr_book)
            counter = 1
            for chapter in chapters:
                chapter.name = request.POST['chapter'+str(counter)]
                chapter.notebook = request.FILES['notebook'+str(counter)]
                dict['chapter'+str(counter)] = chapter.name
                chapter.screen_shots.clear()
                chapter.save()
                counter += 1
            num_new_chapters = curr_book.no_chapters - old_chapter_count
            if num_new_chapters > 0:
                for i in range(num_new_chapters):
                    new_chapter = Chapters()
                    new_chapter.book = curr_book
                    new_chapter.name = request.POST['chapter'+str(counter)]
                    new_chapter.notebook = request.FILES['notebook'+str(counter)]
                    new_chapter.save()
                    counter += 1
            counter = 1
            for screenshot in screen_shots:
                screenshot.caption = request.POST['caption'+str(counter)]
                screenshot.image = request.FILES['image'+str(counter)]
                screenshot.save()
                chapter_image = request.POST['chapter_image'+str(counter)]
                # if chapter name is unique then no need to convert the query
                # set to list. Instead of filter get can be used then.
                chapter = list(Chapters.objects.filter(name=dict[chapter_image]))[-1]
                chapter.screen_shots.add(screenshot)
                chapter.save()
                counter += 1
            curr_proposal.status = "codes submitted"
            curr_proposal.save()
            subject = "Python-TBC: Book & Code Updated"
            message = """Hi """+curr_book.reviewer.name+""",\nA book & code has been updated on the Python TBC interface.\n Details of the book & contributor:\n Contributor: """+curr_book.contributor.user.first_name+""" """+curr_book.contributor.user.last_name+"""\nBook Title"""+curr_book.title+"""\nAuthor: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\nFollow the link to riview the book:\nhttp://tbc-python.fosse.in/book-review/"""+str(curr_book.id)
            add_log(user, curr_book, CHANGE, 'Codes & Screenshots Resubmitted',
                curr_proposal.id)
            email_send(curr_book.reviewer.email, subject, message)
            subject = "Python-TBC: Codes Updated Acknowledgement"
            message = """Hi """+curr_book.contributor.user.first_name+""",\nCodes for the book given below have been successfully updated.\nBook Title: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\n\nPlease be patient while we review your updated codes & get back to you. Review will take a minimum of 25 days. Hoping for kind cooperation."""
        email_send(curr_book.contributor.user.email, subject, message)
        return HttpResponseRedirect('/?bookupdate=done')
    if request.method == 'POST':
        for i in range(1, curr_book.no_chapters+1):
            chapter = Chapters()
            chapter.name = request.POST['chapter'+str(i)]
            dict['chapter'+str(i)] = chapter.name
            chapter.notebook = request.FILES['notebook'+str(i)]
            chapter.book = curr_book
            chapter.save()
        for i in range(1, 4):
            screenshot = ScreenShots()
            screenshot.caption = request.POST['caption'+str(i)]
            screenshot.image = request.FILES['image'+str(i)]
            screenshot.book = curr_book
            screenshot.save()
            chapter_image = request.POST['chapter_image'+str(i)]
            chapter = list(Chapters.objects.filter(name=dict[chapter_image]))[-1]
            chapter.screen_shots.add(screenshot)
            chapter.save()
        curr_proposal.status = "codes submitted"
        curr_proposal.save()
        subject = "Python-TBC: Book Submission"
        message = """Hi """+curr_book.reviewer.name+""",\nA book has been submitted on the Python TBC interface.\n Details of the book & contributor:\n Contributor: """+curr_book.contributor.user.first_name+""" """+curr_book.contributor.user.last_name+"""\nBook Title"""+curr_book.title+"""\nAuthor: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\nFollow the link to riview the book:\nhttp://tbc-python.fosse.in/book-review/"""+str(curr_book.id)
        log_chat = subject + '\n' + 'Book ' + curr_book.title + \
                ' has been submitted on the Python TBC interface.'
        add_log(user, curr_book, CHANGE, 'Chapters and Screenshots added',
                curr_proposal.id, chat=log_chat)
        email_send(curr_book.reviewer.email, subject, message)
        subject = "Python-TBC: Codes Submitted Acknowledgement"
        message = """Hi """+curr_book.contributor.user.first_name+""",\nThank you for your contribution to Python TBC.\nWe have received the book & codes submitted by you.\nDetails of the book are given below: \nBook Title: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\n\nPlease be patient while we review your book & get back to you. Review of the book will take a minimum of 25 days. Hoping for kind cooperation."""
        email_send(curr_book.contributor.user.email, subject, message)
        return HttpResponseRedirect('/?up=done')
    else:
        context.update(csrf(request))
        context['user'] = user
        context['curr_book'] = curr_book
        context['no_notebooks'] = [i for i in range(1, curr_book.no_chapters+1)]
        context['no_images'] = [i for i in range(1, 4)]
        return render_to_response('tbc/upload-content.html', context)


def UpdateContent(request, book_id=None):
    context = {}
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        user = request.user
    current_book = Book.objects.get(id=book_id)
    chapters_to_update = Chapters.objects.filter(book=current_book)
    screenshots_to_update = ScreenShots.objects.filter(book=current_book)
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
        proposal = Proposal.objects.get(accepted=current_book)
        subject = "Python-TBC: Book Updated"
        message = """Hi """+curr_book.reviewer.name+""",\nSubmission for a book has been updated on the Python TBC interface.\n Detailf othe book & contributor: \nContributor: """+curr_book.contributor.user.first_name+""" """+curr_book.contributor.user.last_name+"""\nBook Title"""+curr_book.title+"""\nAuthor: """+curr_book.title+"""\nAuthor: """+curr_book.author+"""\n Publisher: """+curr_book.publisher_place+"""\nISBN: """+curr_book.isbn+"""\nFollow the link to riview the book:\nhttp://tbc-python.fosse.in/book-review/"""+str(curr_book.id)
        log_chat = subject + '\n' + current_book.title +\
                ' book has been updated on the Python TBC interface.'
        add_log(user, current_book, CHANGE, 'book updated', proposal.id,
                chat=log_chat)
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
    file_path = file_path+"/static/Python-Textbook-Companions/"
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
    chapters = Chapters.objects.filter(book=book).order_by('pk')
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
            chapters = Chapters.objects.filter(book=book).order_by('name')
            images = ScreenShots.objects.filter(book=book)
            #for old books (before automated proposal)
            try:
                proposal = Proposal.objects.get(accepted=book)
                logs = ActivityLog.objects.filter(proposal_id=proposal.id)
                context['logs'] = logs
                context['proposal'] = proposal
            except:
                pass
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
            approved_books = Book.objects.filter(approved=True)
            context['approved_books'] = approved_books
            context['books'] = books
            context['reviewer'] = request.user
            context.update(csrf(request))
            return render_to_response('tbc/book-review.html', context)
    else:
        return render_to_response('tbc/forbidden.html')


def ApproveBook(request, book_id=None):
    context = {}
    user = request.user
    if is_reviewer(request.user):
        if request.method == 'POST' and request.POST['approve_notify'] == "approve":
            book = Book.objects.get(id=book_id)
            file_path = local.path
            book_title = book.title.replace(" ", "_")
            directory = file_path+book_title
            os.chdir(directory)
            fp = open(directory+"/README.txt", 'w')
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
            try:
                proposal = Proposal.objects.get(accepted=book)
                proposal.status = "book completed"
                proposal.save()
                msg = "Book Approved"
            except Proposal.DoesNotExist:
                proposal = Proposal()
                proposal.user = book.contributor
                proposal.accepted = book
                proposal.status = "book completed"
                proposal.save()
                msg = "Old Book Approved"
            book.approved = True
            book.save()
            subject = "Python-TBC: Book Completion"
            message = """Hi """+book.contributor.user.first_name+""",\n
Congratulations !\nThe book - """+book.title+""" is now complete & published.\nPlease visit the link given below to download the forms to be filled to complete the formalities.\nhttp://tbc-python.fossee.in/internship-forms\nThe forms should be duly filled (fill only the sections which are applicable) & submitted at the following address:\nDr. Prabhu Ramachandran,\nDepartment of Aerospace Engineering,\nIIT Bombay, Powai, Mumbai - 400076\nKindly write Python Textbook Companion on top of the envelope.\nIf you already sent the forms then you may kindly ignore this mail.\n\nThank You for your contribution !\nRegards,\n Python TBC Team,\nFOSSEE - IIT Bombay"""
            add_log(user, book, CHANGE, msg, proposal.id,
                    chat=subject + '\n' + message)
            email_send(book.contributor.user.email, subject, message)
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
            try:
                proposal = Proposal.objects.get(accepted=book)
                proposal.status = 'codes disapproved'
                proposal.save()
                msg = "Notified Changes"
            except Proposal.DoesNotExist:
                proposal = Proposal()
                proposal.user = book.contributor
                proposal.accepted = book
                proposal.status = 'codes disapproved'
                proposal.save()
                msg = "Notified changes for old book"
            changes_required = request.POST['changes_required']
            subject = "Python-TBC: Corrections Required"
            message = """Hi, """+book.contributor.user.first_name+""",\n\nBook titled, '"""+book.title+"""' requires following changes\n"""+changes_required+"""\n\nKindly make the required corrections and submit the codes again.\n\nRegards,\nPython TBC Team\nFOSSEE - IIT Bombay"""
            context.update(csrf(request))
            add_log(request.user, book, CHANGE, msg,
                    proposal.id, chat=subject+'\n'+changes_required)
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
    context = {}
    path = local.path
    path = path+notebook_path
    notebook_name = path.split("/")[-1:]
    notebook_name = notebook_name[0].split(".")[0]
    path = path.split("/")[0:-1]
    path = "/".join(path)+"/"
    os.chdir(path)
    try:
        template = path+notebook_name+".html"
        return render_to_response(template, {})
    except:
        os.popen("ipython nbconvert --to html \""+path+notebook_name+".ipynb\"")
        template = path+notebook_name+".html"
        return render_to_response(template, {})


def CompletedBooks(request):
    context = {}
    context.update(csrf(request))
    category = "All"
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    if request.method == "POST":
        category = request.POST['category']
        if category == "all":
            completed_books = Book.objects.filter(approved=True)
        else:
            completed_books = Book.objects.filter(category=category, approved=True)
    else:
        completed_books = Book.objects.filter(approved=True)
    context['category'] = category
    context['completed_books'] = completed_books
    return render_to_response('tbc/completed_books.html', context)
    

def BooksUnderProgress(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_anonymous():
        context['anonymous'] = True
    else:
        if is_reviewer(request.user):
            context['reviewer'] = request.user
        else:
            context['user'] = request.user
    if request.method == "POST":
        category = request.POST['category']
        if category == "all":
            books_under_progress = Book.objects.filter(approved=False)
        else:
            books_under_progress = Book.objects.filter(category=category,
                                                       approved=False)
    else:
        books_under_progress = Book.objects.filter(approved=False)
    context['books_under_progress'] = books_under_progress
    return render_to_response('tbc/books_under_progress.html', context)


def GetCertificate(request, book_id=None):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/?require_login=True')
    else:
        user = request.user
    user_profile = Profile.objects.get(user=user)
    books = Book.objects.filter(contributor=user_profile, approved=True)
    context = {}
    context['user'] = user
    context['books'] = books
    error = False
    cur_path = os.path.dirname(os.path.realpath(__file__))
    certificate_path = '{0}/certificate/'.format(cur_path)
    if book_id:
        book = Book.objects.get(id=book_id)
        try:
            proposal_id = Proposal.objects.get(accepted=book_id).id
        except Proposal.DoesNotExist:
            proposal_id = None
        title = book.title
        edition = book.edition
        institute = user_profile.insti_org
        gender = user_profile.gender
        if gender == 'female':
            pronoun = 'She'
        else:
            pronoun = 'He'
        full_name = '%s %s' %(user.first_name, user.last_name)
        user_details = 'from %s' % (institute.replace('&', 'and'))
        book_details = '%s, %s edition' % (title.replace('&', 'and'), edition)
        try:
            template_file = open('{0}template_certificate'.format\
                    (certificate_path), 'r')
            content = string.Template(template_file.read())
            template_file.close()
            content_tex = content.safe_substitute(name=full_name,
                    pronoun=pronoun, details=user_details, book=book_details)
            create_tex = open('{0}tbc_certificate.tex'.format\
                    (certificate_path), 'w')
            create_tex.write(content_tex)
            create_tex.close()
            return_value, err = _make_tbc_certificate(certificate_path)
            if return_value == 0:
                file_name = 'tbc_certificate.pdf'
                pdf = open('{0}{1}'.format(certificate_path, file_name) , 'r')
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; \
                        filename=%s' % (file_name)
                response.write(pdf.read())
                _clean_tbc_certificate(certificate_path)
                add_log(user, book, CHANGE, 'Certificate Downloaded'
                        ,proposal_id)
                return response
            else:
                error = True
                add_log(user, book, CHANGE, err, proposal_id)
        except Exception, e:
            error = True
            add_log(user, book, CHANGE, e, proposal_id)
    
    if error:
        _clean_tbc_certificate(certificate_path)
        context['error'] = error
        return render_to_response('tbc/get-certificate.html', context)
    return render_to_response('tbc/get-certificate.html', context)

def _clean_tbc_certificate(path):
    clean_process = subprocess.Popen('make -C {0} clean'.format(path),
            shell=True)
    clean_process.wait()

def _make_tbc_certificate(path):
    process = subprocess.Popen('timeout 15 make -C {0} tbc'.format(path),
            stderr = subprocess.PIPE, shell = True)
    err = process.communicate()[1]
    return process.returncode, err

def RedirectToIpynb(request, notebook_path=None):
    context = {}
    notebook = notebook_path.split("/")
    notebook[0] = "notebooks"
    notebook = "/".join(notebook)
    redirect_url = "https://ipynb.fossee.in/"+notebook
    return redirect(redirect_url)


# ajax views
@csrf_exempt
def ajax_matching_books(request):
    titles = request.POST["titles"]
    titles = json.loads(titles)
    matches = []
    i = 1
    flag = None
    for title in titles:
        if title:
            match = TempBook.objects.filter(title__icontains=title)
            if match:
                flag = True
                matches.append(match)
            else:
                matches.append(None)
    context = {
        'matches': matches,
        'flag': flag
    }
    return render_to_response('tbc/ajax-matching-books.html', context)
