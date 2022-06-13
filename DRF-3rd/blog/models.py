from django.db import models
from user.models import User as UserModel


class Category(models.Model):
    category_name = models.CharField("카테고리", max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.category_name

class Article(models.Model):
    # 1:N = author:article 관계에서(유저 한명이 여러 게시글 작성 가능)
    # on_delete 옵션 중
    # CASCADE : 작성자(유저) 삭제시 게시글도 삭제
    # PROTECT : 게시글 있으면 작성자(유저) 삭제 불가
    # SET_DEFAULT(default 옵션을 꼭 추가해야 한다) : 작성자(유저) 삭제시 삭제된 작성자 대신 미리 지정해둔 임의의 값을 넣고 게시글 유지
    author = models.ForeignKey(to=UserModel, verbose_name='작성자', related_name='author', on_delete=models.SET_DEFAULT, default='ghost')
    title = models.CharField("제목", max_length=200)
    # 참조해준 객체 입장에서 related_name을 설정
    category = models.ManyToManyField(to=Category, verbose_name='카테고리', related_name='category')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}"
    