from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^new/$', 'comments.views.new_comment', name='new_comment'),
    url(r'^get/$', 'comments.views.get_comments', name='new_comment'),
    url(r'^new-reply/$', 'comments.views.new_reply', name='new_reply'),
)
