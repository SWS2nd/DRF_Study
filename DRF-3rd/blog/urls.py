from django.urls import path
from blog.views import MainPost as MainPostModel
from blog.views import WritePost as WritePostModel

app_name = "blog"

urlpatterns = [
    path('', MainPostModel.as_view(), name='home'),
    path('writepost/', WritePostModel.as_view(), name='writepost'),
]
