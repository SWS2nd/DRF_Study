from django.urls import path
from user.views import HelloWorld
from user.views import Login as LoginModel
from user.views import Logout as LogoutModel
from user.views import SignUp as SignUpModel
from user.views import UserInformation as UserInformationModel

app_name = "user"

urlpatterns = [
    # 127.0.0.1:8000/helloworld 테스트용
    path('helloworld/', HelloWorld.as_view()),
    path('login/', LoginModel.as_view(), name='login'),
    path('logout/', LogoutModel.as_view(), name='logout'),
    path('sign-up/', SignUpModel.as_view(), name='sign-up'),
    path('user-inform/', UserInformationModel.as_view(), name='user-inform'),
]
