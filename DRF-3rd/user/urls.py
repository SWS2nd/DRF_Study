from django.urls import path
from user.views import HelloWorld


urlpatterns = [
    # 127.0.0.1:8000/user/helloworld 테스트용
    path('helloworld/', HelloWorld.as_view()),
]
