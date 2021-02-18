from django.urls import path
from parser_backend import views

urlpatterns = [
    path('', views.main_rss, name="parser_backend"),
    path('post-<int:pk>', views.open_feed, name="open_feed")
    #path("favicon.ico", views.serve_favicon, name="serve_favicon") #and this is trash too!
]