from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework import permissions

from blog.models import Article as ArticleModel
from blog.models import Category as CategoryModel


# 커스텀 퍼미션
class MyCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # 요청한 user 존재, 로그인된 user, user의 permission_rank가 5 초과인 경우 통과되도록 권한 custom 
        result = bool(user and user.is_authenticated and user.permission_rank > 5)
        return result

# 메인 페이지
class MainPost(APIView):
    def get(self, request):
        user = request.user.is_authenticated
        if user:
            all_post = ArticleModel.objects.all().order_by('-created_at')
            return render(request, 'blog/main.html', {'posts': all_post})
        else:
            return redirect('user:login')

# 글 작성
class WritePost(APIView):
    def get(self, request):
        user = request.user.is_authenticated
        if user:
            return render(request, 'blog/write_post.html')
        else:
            return redirect('user:login')
    def post(self, request):
        permission_classes = [MyCustomPermission]
        user = request.user
        # request.data : 아무 데이터나 다룰 수 있고, 'POST'뿐만 아니라 'PUT'과 'PATCH' 메서드에서도 사용 가능
        title = request.data.get('title', '')
        content = request.data.get('my-content', '')
        categorys = request.data.get('category', '').split(',')
        
        if content == '':
            messages.error(request, '글은 공백일 수 없습니다.')
            return redirect('blog:writepost')
        else:
            my_post = ArticleModel.objects.create(author=user, title=title, content=content)
            for category in categorys:
                # 카테고리가 있다면
                if category != '':
                    # 문자열 양쪽 공백 제거를 위해 .strip() 사용
                    category = category.strip()
                    # objects.get_or_create 메소드는 두 개의 값을 반환하며,
                    # created는 해당 카테고리가 기존에 있던 카테고리인지(True) 새로 생성된 카테고리인지(False)의 Boolean 값을 반환하고. 
                    # category_는 True라면 새로 생성한 카테고리값이고 False라면 기존 DB에서 가져온 카테고리 값을 반환
                    category_, created = CategoryModel.objects.get_or_create(category_name=category)
                    # my_post 객체의 categorys 필드에 category value 값을 추가
                    my_post.category.add(category_)
            my_post.save()
            return redirect('blog:home')
        