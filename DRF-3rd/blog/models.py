from django.db import models
from user.models import User as UserModel


class Category(models.Model):
    category_name = models.CharField("카테고리 이름", max_length=20, unique=True)
    description = models.TextField()

class Article(models.Model):
    author = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='author')
    title = models.CharField("제목", max_length=200)
    # 참조해준 객체 입장에서 related_name을 설정
    category = models.ManyToManyField(to=Category, verbose_name='카테고리', related_name='category')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    