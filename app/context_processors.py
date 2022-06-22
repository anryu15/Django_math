from django.db.models import Count
from app.models import Category, SubCategory


def common(request):
    context = {
        'categories': Category.objects.annotate(num_posts=Count('post')),
        'subcategories': SubCategory.objects.annotate(num_posts=Count('post')),
    }
    return context