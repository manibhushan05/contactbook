from django.urls import path, re_path

from . import views

urlpatterns = [
    # Contact Book URLS
    re_path(r'^contact-book-list/$', views.ContactBookListView.as_view(), name='contact_book_list'),
    re_path(r'^contact-book-create/$', views.ContactBookViewSet.as_view(
        {'post': 'create'}), name='contact_book_create'),
    re_path(r'^contact-book-retrieve/(?P<pk>[0-9]+)/$', views.ContactBookViewSet.as_view(
        {'get': 'retrieve'}), name='contact_book_retrieve'),
    re_path(r'^contact-book-update/(?P<pk>[0-9]+)/$', views.ContactBookViewSet.as_view(
        {'put': 'update'}), name='contact_book_update'),
    re_path(r'^contact-book-partial-update/(?P<pk>[0-9]+)/$', views.ContactBookViewSet.as_view(
        {'patch': 'partial_update'}), name='contact_book_partial_update'),
    re_path(r'^contact-book-soft-delete/(?P<pk>[0-9]+)/$', views.ContactBookViewSet.as_view(
        {'delete': 'soft_delete'}), name='contact_book_soft_delete'),
    re_path(r'^contact-book-hard-delete/(?P<pk>[0-9]+)/$', views.ContactBookViewSet.as_view(
        {'delete': 'hard_delete'}), name='contact_book_hard_delete/'),

    # Contact  URLS
    re_path(r'^contact-list/$', views.ContactListView.as_view(), name='contact_list'),
    re_path(r'^contact-create/$', views.ContactViewSet.as_view(
        {'post': 'create'}), name='contact_create'),
    re_path(r'^contact-retrieve/(?P<pk>[0-9]+)/$', views.ContactViewSet.as_view(
        {'get': 'retrieve'}), name='contact_retrieve'),
    re_path(r'^contact-update/(?P<pk>[0-9]+)/$', views.ContactViewSet.as_view(
        {'put': 'update'}), name='contact_update'),
    re_path(r'^contact-partial-update/(?P<pk>[0-9]+)/$', views.ContactViewSet.as_view(
        {'patch': 'partial_update'}), name='contact_partial_update'),
    re_path(r'^contact-soft-delete/(?P<pk>[0-9]+)/$', views.ContactViewSet.as_view(
        {'delete': 'soft_delete'}), name='contact_soft_delete'),
    re_path(r'^contact-hard-delete/(?P<pk>[0-9]+)/$', views.ContactViewSet.as_view(
        {'delete': 'hard_delete'}), name='contact_hard_delete'),

    # authentication
    re_path(r'^login/$', views.UserLogin.as_view(), name='login'),
    re_path(r'^logout/$', views.UserLogout.as_view(), name='logout'),
]
