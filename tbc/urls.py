from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Home page
    url(r'^$', 'tbc.views.Home', name='Home'),
    url(r'^register/$', 'tbc.views.UserRegister', name='UserRegister'),
    url(r'^login/$', 'tbc.views.UserLogin', name='UserLogin'),
    url(r'^logout/$', 'tbc.views.UserLogout', name='UserLogout'),
    url(r'^profile/$', 'tbc.views.UserProfile', name='UserProfile'),
    url(r'^submit-book/$', 'tbc.views.SubmitBook', name='SubmitBook'),
    url(r'^upload-chapters/$', 'tbc.views.ChapterUpload', name='ChapterUpload'),
    url(r'^get-zip/(?P<book_id>\d+)$', 'tbc.views.GetZip', name='GetZip'),
    url(r'^upload-images/$', 'tbc.views.ImageUpload', name='ImageUpload'),
    url(r'^browse-books/$', 'tbc.views.BrowseBooks', name='BrowseBooks'),
    url(r'^book-details/(?P<book_id>\d+)/$', 'tbc.views.BookDetails', name='BookDetails'),
)
