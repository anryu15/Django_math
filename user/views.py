from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView # テンプレートタグ
from .forms import AccountUserForm, AddAccountUserForm # ユーザーアカウントフォーム
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


import sys
sys.path.append('../')
from config.config import *
from app.models import Post,Category,SubCategory
#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('home'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'user/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))


#ホーム
@login_required
def home(request):
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

    # params = {"UserID":request.user,}
    # return render(request, "user/home.html",context=params)
    # return render(request, "user/home.html",context=params)



class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountUserForm(),
        "add_account_form":AddAccountUserForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountUserForm()
        self.params["add_account_form"] = AddAccountUserForm()
        self.params["AccountCreate"] = False
        return render(request,"user/register.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountUserForm(data=request.POST)
        self.params["add_account_form"] = AddAccountUserForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            # if 'account_image' in request.FILES:
            #     add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        print("wwqw")
        login(request, account)
        return redirect('index')
        # return render(request,"user/register.html",context=self.params)