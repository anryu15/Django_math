from django.contrib import admin
from .models import Post
from .models import Comment
from .models import Category
from .models import SubCategory
from .models import ReportCategory
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ReportCategory)