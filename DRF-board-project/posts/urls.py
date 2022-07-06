from django.urls import path
from rest_framework import routers # viewsets과 같이 사용됨.

from .views import PostViewSet


router = routers.SimpleRouter
router.register('posts', PostViewSet)

urlpatterns = router.urls
