import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from comments.forms import CommentForm, ReplyForm
from comments.models import Comment, Reply

def get_comments(request):
    # retriving comment parameters
    book = request.GET.get('book', '')
    chapter = request.GET.get('chapter', '')
    example = request.GET.get('example', '')
    page = request.GET.get('page', '')
    comments = Comment.objects.filter(book=book).filter(chapter=chapter).filter(example=example)
    context = {
        'comments': comments,
        'book': book,
        'chapter': chapter,
        'example': example,
        'page': page
    }
    return render(request, "comments/get_comments.html", context)

def new_comment(request):
    # saving the poted comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.book = form.cleaned_data.get("book")
            comment.chapter = form.cleaned_data.get("chapter")
            comment.example = form.cleaned_data.get("example")
            comment.page = form.cleaned_data.get("page")
            comment.title = form.cleaned_data.get("title")
            comment.body = form.cleaned_data.get("body")
            comment.email = form.cleaned_data.get("email")
            comment.save()
            return HttpResponseRedirect(
                '/comments/get/?book={0}&chapter={1}&example={2}&page={3}'.format(
                    comment.book, comment.chapter, comment.example, comment.page
                )
            )
        else:
            book = request.POST.get('book', '')
            chapter = request.POST.get('chapter', '')
            example = request.POST.get('example', '')
            page = request.POST.get('page', '')
            return HttpResponseRedirect(
                '/comments/new/?book={0}&chapter={1}&example={2}&page={3}'.format(
                    book, chapter, example, page
                )
            )

    # retriving comment parameters
    book = request.GET.get('book', '')
    chapter = request.GET.get('chapter', '')
    example = request.GET.get('example', '')
    page = request.GET.get('page', '')
    initial_values = {
        'book': book,
        'chapter': chapter,
        'example': example,
        'page': page
    }
    form = CommentForm(initial = initial_values)
    context = {
        'form': form,
        'book': book,
        'chapter': chapter,
        'example': example,
        'page': page
    }
    context.update(csrf(request))
    return render(request, 'comments/new_comment.html', context)

def new_reply(request):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment_id  = form.cleaned_data.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            reply = Reply()
            reply.comment = comment
            reply.body = form.cleaned_data.get('body')
            reply.email = form.cleaned_data.get('email')
            reply.save()
            return HttpResponseRedirect(
                '/comments/get/?book={0}&chapter={1}&example={2}&page={3}'.format(
                    comment.book, comment.chapter, comment.example, comment.page
                )
            )
        else:
            comment_id = request.POST.get('comment_id', '')
            return HttpResponseRedirect(
                '/comments/new-reply/?comment_id={0}'.format(
                    comment_id
                )
            )
    comment_id = request.GET.get('comment_id', '')
    comment = Comment.objects.get(id=comment_id)
    initial_values = {
        'comment_id': comment_id
    }
    form = ReplyForm(initial = initial_values)
    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'comments/new_reply.html', context)
