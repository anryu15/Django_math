from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>', views.good, name="post_detail_good"),
    path('post/<int:pk1>/comment/<int:pk2>/add_good', views.AddGood.as_view(), name="add_good"),
    path('post/<int:pk1>/comment/<int:pk2>', views.CommentDetailView.as_view(), name="comment_detail"),
    # path('post/<int:pk>', views.badcom, name="post_detail_badcomment"),
    # path('post/<int:pk>', views.goodcom, name="post_detail_goodcomment"),
    path('post/new', views.CreatePostView.as_view(), name="post_new"),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name="post_edit"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<str:category_slug>/',views.CategoryPostView.as_view(), name='category_post'),
    path('mypage/<int:pk>/',views.MyPageView.as_view(), name='mypage'),
    path('subcategories/', views.SubCategoryListView.as_view(), name='subcategory_list'),
    path('subcategory/<str:subcategory_slug>/',views.SubCategoryPostView.as_view(), name='subcategory_post'),
    # コメント追加
    path('post/<int:pk>/new_comment', views.AddCommentView.as_view(), name="add_comment"),
    path('post/<int:po>/<int:co>', views.ReportView.as_view(), name="report_comment"),
    path('post/<int:po>/<int:co>', views.ReportView.as_view(), name="comment_report"),
    #説明
    path('explain', views.ExplainView.as_view(), name="explain"),
    #他人の投稿一覧
    path('other_post/<int:pk>',views.OtherPostView.as_view(),name="other_post"),
    path('other_post2/<int:pk>',views.OtherPostView2.as_view(),name="other_post2"),
    # 利用規約
    path('service',views.ServiceView.as_view(),name="service")
]