# from config.config import to_dict
from click import command
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View,ListView
# from gevent import config
from .models import Post,Category,SubCategory
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django import forms
from django.views.decorators.http import require_POST
from django.http import HttpResponse


from django.http import Http404
from django.http.response import JsonResponse


from .models import Comment, ReportCategory
from .forms import CommentForm
from .forms import CommentReportForm
from .forms import CommentReportCategoryForm

import re

import sys
sys.path.append('../')
from config.config import *
from user.models import AccountUser


class IndexView(View):
    def get(self, request, *args, **kwargs): #最初に呼ばれる関数
        login_user = request.user
        post_data = Post.objects.order_by('-id')
        print(len(post_data))
        # print(post_data[0].content)
        for data in post_data:
            f = Functions()
            Dict = f.to_dict(data.content)
            data.content = Dict
            print(data.content)
        # comment_num
        return render(request, 'app/index.html', {'post_data': post_data ,'login_user':login_user})

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_id = post_data.id
        # 投稿
        f = Functions()
        Dict = f.to_dict(post_data.content)

        comment_data = post_data.comments.all()
# -----------------------------------------------------------修正
        for i in comment_data:
            tmpDict = {}
            # print(type(i.body))
            i_array = i.body.split("'''")
            i_mark_array = re.findall(r"'''(.*?)'''",i.body)
            for data in i_array:
                if data in i_mark_array:
                    tmpDict[data] = 1
                else:
                    tmpDict[data] = 0
            i.body = tmpDict
        author_id = post_data.author.id
        
# -----------------------------------------------------------修正
        return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data, 'post_data_dict': Dict, 'post_id':post_id, 'author_id': author_id})

    def post(self, request, *args, **kwargs): #ボタンクリック時
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST)
        

        print("postdetailview post")
        if request.method == 'POST':
            if 'good' in request.POST:
                print("in post method")
                goodlist = request.user.get_username()
                print(request.user.id)
                print(post_data.author.id)
                users = AccountUser.objects.all()
                Author = AccountUser.objects.get(id=post_data.author.id-1)
                print("Au")
                if goodlist in post_data.goodtext:
                    print("goodlist")
                    pass
                else:
                    print("else")
                    post_data.good += 1
                    post_data.goodtext +=  " " + goodlist
                    post_data.save()
                    Author.numgood += 1
                    print("--------")
                    print(Author.numgood)
                    Author.save()
                
                print("f")
                f = Functions()
                Dict = f.to_dict(post_data.content)
                
                comment_data = post_data.comments.all()
                print("comment_data")
                for i in comment_data:
                    print("tmpDict")
                    tmpDict = {}
                    i_array = i.body.split("$")
                    i_mark_array = re.findall(r"$(.*?)$",i.body)
                    for data in i_array:
                        if data in i_mark_array:
                            tmpDict[data] = 1
                        else:
                            tmpDict[data] = 0
                    i.body = tmpDict
                print("return")
                return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data, 'post_data_dict': Dict,})
            


        # 有効か
        if form.is_valid():
            print("comment save")
            comment_data = Comment()
            comment_data.post = Post.objects.get(id=self.kwargs['pk'])
            comment_data.author = request.user
            comment_data.body = form.cleaned_data['body']
            comment_data.save()
            return redirect("post_detail", post_data.id)
        return render(request, "app/post_detail.html", {"form":form})



class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        categorylst=Category.objects.all()
        subcategorylst=SubCategory.objects.all()
        return render(request, 'app/post_form.html', {'form': form,'categoryList' : categorylst, 'subcategoryList':subcategorylst})

    def post(self, request, *args, **kwargs): #ボタンクリック時
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post_data = Post()
            print("aaa2")
            post_data.author = request.user #ログインユーザ
            post_data.title = form.cleaned_data['title']
            post_data.img = form.cleaned_data['img']
            # post_data.img = request.FILES['img']
            post_data.content = form.cleaned_data['content'] #formから取得
    
    # 二段回プルダウン---

            categorylst = Category.objects.all()
            for category in categorylst:
                if category.name == form.cleaned_data['category']:
                    cat = Category.objects.get(id=category.id)
            subcategorylst = SubCategory.objects.all()
            for subcategory in subcategorylst:
                if subcategory.name == form.cleaned_data['subcategory']:
                    sucat = SubCategory.objects.get(id=subcategory.id)
            
            post_data.category = cat
            post_data.subcategory = sucat
    # 二段回プルダウン---
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {'form': form})

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'content': post_data.content,
                'category': post_data.category,
                'subcategory': post_data.subcategory
            }
        )
        categorylst=Category.objects.all()
        subcategorylst=SubCategory.objects.all()
        return render(request, 'app/post_form.html', {'form': form,'categoryList' : categorylst, 'subcategoryList':subcategorylst})


    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content'] #formから取得
            # choicefield追加
            lst=Category.objects.all()
            for i in range(len(lst)):
                if lst[i].name==form.cleaned_data['category']:
                    break
            cat=Category.objects.get(id=i+1)
            cat.name=form.cleaned_data['category']
            post_data.category = cat
            lst2=SubCategory.objects.all()
            for j in range(len(lst2)):
                if lst2[j].name==form.cleaned_data['subcategory']:
                    break
            sub_cat=SubCategory.objects.get(id=j+1)
            sub_cat.name=form.cleaned_data['subcategory']
            post_data.subcategory = sub_cat
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {'form': form})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {'post_data': post_data})

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')
    

class CategoryListView(ListView):
    queryset = Category.objects.annotate(num_posts=Count('post'))

class CategoryPostView(ListView):
    model = Post
    template_name = 'app/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# tex
class MyPageView(View):
    def get(self, request, *args, **kwargs):
        print("-------!!!!-----")
        print(self.kwargs['pk'])
        try:
            my_post = Post.objects.filter(author=self.kwargs['pk'])
            for data in my_post:
                f = Functions()
                Dict = f.to_dict(data.content)
                data.content = Dict
        except Post.DoesNotExist:
            my_post = None
        # login_user = request.user
        
        print(request.user.id)
        print("---------------------")
        Author = AccountUser.objects.all()
        login_user = AccountUser.objects.get(id=self.kwargs['pk']-1)
        print(login_user.contents)
        return render(request, 'app/mypage.html', {'my_post': my_post,'login_user': login_user})



def good(self, request):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        print(post_data.author)
        comment_data = post_data.comments.all()
        # print("aabbcc")
        print("in the good")
        print("good method")
        # return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data})
        if request.method == 'POST':
            if 'good' in request.POST:
                print(request.user.get_username())
                print("aabbccdd")
                goodlist = request.user.get_username()
                print(request.user.id)
                
                if goodlist in post_data.goodtext:
                    pass
                else:
                    post_data.good += 1
                    post_data.goodtext +=  " " + goodlist
                    post_data.save()
                return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data})



class SubCategoryListView(ListView):
    queryset = SubCategory.objects.annotate(num_posts=Count('post'))

class SubCategoryPostView(ListView):
    model = Post
    template_name = 'app/subcategory_post.html'

    def get_queryset(self):
        subcategory_slug = self.kwargs['subcategory_slug']
        self.subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        qs = super().get_queryset().filter(subcategory=self.subcategory)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        return context

class AddCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST or None)
        f = Functions()
        Dict = f.to_dict(post_data.content)

        return render(request, 'app/comment_form.html', {'form': form,'post_data': post_data, 'post_data_dict': Dict,})

    def post(self, request, *args, **kwargs): #ボタンクリック時
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST)
        # 有効か
        if form.is_valid():
            print("comment save")
            comment_data = Comment()
            comment_data.post = Post.objects.get(id=self.kwargs['pk'])
            comment_data.author = request.user
            comment_data.body = form.cleaned_data['body']
            comment_data.save()
            post_data.numComment += 1
            post_data.save()
            return redirect("post_detail", post_data.id)
        return render(request, "app/post_detail.html", {"form":form})

class ReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CommentReportCategoryForm(request.POST or None)
        post_data = Post.objects.get(id=self.kwargs['po'])
        post_id = post_data.id
        # 投稿
        report_content = ReportCategory.objects.all()
        f = Functions()
        Dict = f.to_dict(post_data.content)

        comment_data = Comment.objects.get(id=self.kwargs['co'])
        comment_Dict = f.to_dict(comment_data.body)
        return render(request, 'app/comment_report.html', {'form': form, 'post_data': post_data, 'comment_data': comment_data, 'post_data_dict': Dict, 'comment_Dict':comment_Dict,'report_data':report_content})

    def post(self, request, *args, **kwargs): #ボタンクリック時
        post_data = Post.objects.get(id=self.kwargs['po'])
        comment_data = Comment.objects.get(id=self.kwargs['co'])
       
        form = CommentForm(request.POST)
        print("add report--------------")
        # print(form.cleaned_data['report'])
        check = request.POST.getlist("report")
        print(check)
        userlist = request.user.get_username()

        comment_data.report_content +=  " " + str(check)
        comment_data.reportlist += " " + str(userlist)
        comment_data.save()
        return redirect("post_detail", post_data.id)
        # return render(request, 'app/post_detail.html', {'post_data': post_data})

class ExplainView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
         return render(request, 'app/explain.html')
        # return redirect("explain")
        

class AddGood(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk1'])
        comment_data = Comment.objects.get(id=self.kwargs['pk2'])
        return render(request,'app/good_btn.html',{'post_data': post_data,'comment_data': comment_data})

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk1'])
        comment_data = post_data.comments.all()
        com = Comment.objects.get(id=self.kwargs['pk2'])
        couneter=0
        for i in range(len(comment_data)):
            if comment_data[i].id == self.kwargs['pk2']:
                couneter=i
                break
        result=request.POST.getlist("evaluate")
        # 1=good 2=bad
        if '1' in result:
            lst=request.user.get_username()
            if lst in com.goodcommenttext:
                pass
            elif lst in com.badcommenttext:
                pass
            else:
                comment_data[couneter].goodcomment+=1
                comment_data[couneter].goodcommenttext+=" "+lst
                comment_data[couneter].save()
            # return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data})
            
            # return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data})
        elif '2' in result:
            lst=request.user.get_username()
            if lst in com.badcommenttext:
                pass
            elif lst in com.goodcommenttext:
                pass
            else:
                comment_data[couneter].badcomment+=1
                comment_data[couneter].badcommenttext+=" "+lst
                comment_data[couneter].save()

        elif '3' in result:
            lst=request.user.get_username()
            str_lst=str(lst)
            comment_data[couneter].goodcomment-=1
            comment_data[couneter].goodcommenttext=comment_data[couneter].goodcommenttext.replace(str_lst, '')
            comment_data[couneter].save()
        
        else:
            lst=request.user.get_username()
            str_lst=str(lst)
            comment_data[couneter].badcomment-=1
            comment_data[couneter].badcommenttext=comment_data[couneter].badcommenttext.replace(str_lst, '')
            comment_data[couneter].save()

        return redirect("post_detail", post_data.id)
        # return render(request, 'app/post_detail.html', {'post_data': post_data, 'comment_data': comment_data})
        # return redirect("post_detail", post_data.id)

class CommentDetailView(View):
    def get(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['pk2'])
        com_id=comment_data.id
        post_data=Post.objects.get(id=self.kwargs['pk1'])
        pos_id=post_data.id
        # 投稿
        f = Functions()
        Dict = f.to_dict(comment_data.body)
        tmpDict = {}
        com_array = comment_data.body.split("'''")
        com_mark_array = re.findall(r"'''(.*?)'''",comment_data.body)
        for data in com_array:
                if data in com_mark_array:
                    tmpDict[data] = 1
                else:
                    tmpDict[data] = 0
                comment_data.body = tmpDict
        goodlst=comment_data.goodcommenttext
        badlst=comment_data.badcommenttext
        #print("goodlst:",goodlst)
        #print("badlst:",badlst)
        login_user = request.user
        str_user=str(login_user)
        return render(request, 'app/comment_detail.html', {'comment_data': comment_data, 
                                                           'comment_data_dict': Dict, 
                                                           'comment_id':com_id,
                                                           'post_id':pos_id,'post_data':post_data,
                                                           'user':str_user,
                                                           'good_list':goodlst,
                                                           'bad_list':badlst,
                                                           })

class OtherPostView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        author = post_data.author
        author_data = AccountUser.objects.get(id=author.id-1)
        #print(author)
        posts = Post.objects.filter(author=author)
        #print(posts)
        login_user = request.user
        if author==login_user:
            return render(request, 'app/mypage.html', {'my_post': posts,'login_user': login_user})
        else:
            return render(request, 'app/other_post.html', {'posts': posts,'author': author, 'author_data':author_data})

# tex
class OtherPostView2(View):
    def get(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['pk'])
        author = comment_data.author
        author_data = AccountUser.objects.get(id=author.id-1)
        print(author)
        posts = Post.objects.filter(author=author)
        for data in posts:
            f = Functions()
            Dict = f.to_dict(data.content)
            data.content = Dict
        print(posts)
        login_user = request.user
        if author==login_user:
            return render(request, 'app/mypage.html', {'my_post': posts,'login_user': login_user})
        else:
            return render(request, 'app/other_post.html', {'posts': posts,'author': author,'author_data':author_data})

class ServiceView(View):
    def get(self, request, *args, **kwargs):
         return render(request, 'app/termsOfService.html')