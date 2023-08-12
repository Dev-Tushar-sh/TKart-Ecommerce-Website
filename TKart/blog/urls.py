from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="BlogHome"),
    path("blogpost/",views.blogpost ,name="blogPost"),
    path("blogpost/<int:id>",views.blogpost ,name="blogPost")
]
