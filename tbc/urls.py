from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'tbc.views.home', name='home'),
    url(r'^internship-forms/$', 'tbc.views.internship_forms', name='internship_forms'),
    url(r'^about-pythontbc/$', 'tbc.views.about_pytbc', name='about_pytbc'),
   
    url(r'^sample-notebook/$', 'tbc.views.sample_ipynb', name='sample_ipynb'),
    url(r'^register/$', 'tbc.views.user_register', name='user_register'),
    url(r'^login/$', 'tbc.views.user_login', name='user_login'),
    url(r'^logout/$', 'tbc.views.user_logout', name='user_logout'),
    url(r'^profile/$', 'tbc.views.user_profile', name='user_profile'),
    url(r'^update-profile/$', 'tbc.views.update_profile', name='update_profile'),
    url(r'^forgot-password/$', 'tbc.views.forgot_password', name='forgot_password'),
    url(r'^update-password/$', 'tbc.views.update_password', name='update_password'),
    url(r'^admin-tools/$', 'tbc.views.admin_tools', name='admin_tools'),    
   
    url(r'^submit-proposal/$', 'tbc.views.submit_proposal', name='submit_proposal'),
    url(r'^submit-aicte-proposal/$', 'tbc.views.list_aicte', name='list_aicte'),
    url(r'^submit-aicte-proposal/(?P<aicte_book_id>\d+)/$', 'tbc.views.submit_aicte_proposal', name='submit_aicte_proposal'),
    url(r'^submit-book/$', 'tbc.views.submit_book', name='submit_book'),
    url(r'^submit-sample/$', 'tbc.views.submit_sample', name='submit_sample'),
    url(r'^submit-sample/(?P<proposal_id>\d+)$', 'tbc.views.submit_sample', name='submit_sample'),
    url(r'^submit-sample/(?P<proposal_id>\d+)/(?P<old_notebook_id>\d+)$', 'tbc.views.submit_sample', name='submit_sample'),
    url(r'^confirm-book-details/$', 'tbc.views.confirm_book_details', name='confirm_book_details'),
    url(r'^submit-book-old/$', 'tbc.views.submit_book', name='submit_book'),
    url(r'^submit-code/$', 'tbc.views.submit_code', name='submit_code'),
    url(r'^submit-code-old/(?P<book_id>\d+)$', 'tbc.views.submit_code_old', name='submit_code_old'),
    url(r'^update-content/(?P<book_id>\d+)$', 'tbc.views.update_content', name='update_content'),
    url(r'^get-zip/(?P<book_id>\d+)$', 'tbc.views.get_zip', name='get_zip'),
    url(r'^browse-books/$', 'tbc.views.browse_books', name='browse_books'),
    url(r'^browse-books/(?P<category>.+)$', 'tbc.views.browse_books', name='browse_books'),
    url(r'^convert-notebook/(?P<notebook_path>.+)$', 'tbc.views.convert_notebook', name='convert_notebook'),
    url(r'^book-details/(?P<book_id>\d+)/$', 'tbc.views.book_details', name='book_details'),
	url(r'^completed-books/$', 'tbc.views.completed_books', name='completed_books'),
	url(r'^completed-books/(?P<category>.+)$', 'tbc.views.completed_books', name='completed_books'),
	url(r'^books-under-progress/$', 'tbc.views.books_under_progress', name='books_under_progress'),
	url(r'^redirect-ipynb/(?P<notebook_path>.+)$', 'tbc.views.redirect_to_ipynb', name='redirect_to_ipynb'),
	url(r'^get-certificate/$', 'tbc.views.get_certificate', name='get_certificate'),
	url(r'^get-certificate/(?P<book_id>\d+)/$', 'tbc.views.get_certificate', name='get_certificate'),
    
    
    url(r'^book-review/$', 'tbc.views.book_review', name='book_review'),
    url(r'^proposal-review/$', 'tbc.views.review_proposals', name='review_proposals'),
    url(r'^proposal-review/(?P<proposal_id>\d+)/(?P<textbook_id>\d+)$', 'tbc.views.review_proposals', name='review_proposals'),
    url(r'^disapprove-sample-notebook/(?P<proposal_id>\d+)$', 'tbc.views.disapprove_proposal', name='disapprove_proposal'),
    url(r'^allot-book/(?P<proposal_id>\d+)$', 'tbc.views.allot_book', name='allot_book'),
    url(r'^reject-proposal/(?P<proposal_id>\d+)$', 'tbc.views.reject_proposal', name='reject_proposal'),
    url(r'^book-review/(?P<book_id>\d+)$', 'tbc.views.book_review', name='book_review'),
    url(r'^approve-book/(?P<book_id>\d+)$', 'tbc.views.approve_book', name='approve_book'),
    url(r'^notify-changes/(?P<book_id>\d+)$', 'tbc.views.notify_changes', name='notify_changes'),
    url(r'^brokenbooks/$', 'tbc.views.get_broken_books', name='broken_books'),
    url(r'^link-image/$', 'tbc.views.link_image', name='link_image'),

    # ajax urls
    url(r'^ajax/matching-books/$', 'tbc.views.ajax_matching_books', name='AjaxMatchingBooks'),

)
