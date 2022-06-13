from django.contrib import admin
from blog.models import Category as CategoryModel
from blog.models import Article as ArticleModel


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']

# ArticleModel 모델에 위에서 정의한 ArticleModelAdmin 설정을 가져다 쓸 것임
admin.site.register(ArticleModel, ArticleModelAdmin)

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']

# CategoryModel 모델에 위에서 정의한 CategoryModelAdmin 설정을 가져다 쓸 것임
admin.site.register(CategoryModel, CategoryModelAdmin)