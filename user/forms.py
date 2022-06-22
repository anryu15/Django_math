from django import forms
from django.contrib.auth.models import User
from .models import AccountUser

# フォームクラス作成
class AccountUserForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AddAccountUserForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = AccountUser
        fields = ('contents',)
        labels = {'contents':"紹介文",}