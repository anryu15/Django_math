from cProfile import label
from django import forms
from PIL import Image


class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    img = forms.ImageField(label='img',required=False)
    content = forms.CharField(label='内容', widget=forms.Textarea())
    category = forms.CharField(max_length=10, label='カテゴリー')
    subcategory = forms.CharField(max_length=10, label='サブカテゴリー')
    
class CommentForm(forms.Form):
    body = forms.CharField(label='内容', widget=forms.Textarea())

class CommentReportForm(forms.Form):
    report_content = forms.CharField(label="report_content")

class CommentReportCategoryForm(forms.Form):
    name = forms.CharField(max_length=50, label='報告内容')
