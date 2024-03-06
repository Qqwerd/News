from django.urls import path
from .views import NewsList, NewsItem, Search, CreatePost, EditPost, DeletePost, add_subscribe, del_subscribe, logging_page, test_error

from django.urls import path
from .views import my_view

urlpatterns = [
  path('my-view/', my_view, name='my_view'),
]

urlpatterns = [
  path('', NewsList.as_view()),
  path('<int:pk>', NewsItem.as_view()),
  path('search', Search.as_view()),
  path('add', CreatePost.as_view()),
  path('<int:pk>/edit', EditPost.as_view()),
  path('<int:pk>/delete', DeletePost.as_view()),
  path('<int:pk>/add_subscribe', add_subscribe),
  path('<int:pk>/del_subscribe', del_subscribe),
  path('logging_page/', logging_page, name='logging_page'),
  path('test_error', test_error, name='test_error'),

]