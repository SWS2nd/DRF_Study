from django.contrib import admin
from blog.models import Category as CategoryModel
from blog.models import Article as ArticleModel


# register Category Model in user app
admin.site.register(CategoryModel)
# register Article Model in user app
admin.site.register(ArticleModel)
