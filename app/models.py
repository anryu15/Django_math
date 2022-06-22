from django.db import models
from django.conf import settings
from django.utils import timezone

# root
# Passwordroot
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=255)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    img = models.ImageField(blank=True, null=True, upload_to = 'media/')
    good = models.IntegerField('Good',default=0)  # 追加が必要な箇所。いいねの数を記事に紐づけて保存する
    goodtext = models.TextField("リスト")
    numComment = models.IntegerField('comment',default=0)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField() 
    posted_date = models.DateTimeField(auto_now_add=True)   
    goodcomment = models.IntegerField('GoodComment',default=0)  # 追加が必要な箇所。いいねの数を記事に紐づけて保存する
    goodcommenttext = models.TextField("goodコメントリスト")
    badcomment = models.IntegerField('BadComment',default=0)  # 追加が必要な箇所。いいねの数を記事に紐づけて保存する
    badcommenttext = models.TextField("badコメントリスト")
    reportlist = models.TextField("reportリスト")
    report_content = models.TextField("report_content")

class ReportCategory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
