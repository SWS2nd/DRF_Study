from django.urls import path
from rest_framework import routers # viewsets과 같이 사용됨.

from .views import PostViewSet, like_post


router = routers.SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = router.urls + [
    path('like/<int:pk>/', like_post, name='like_post')
]
