from django.urls import path
from jantama_app import views


app_name = 'jantama_app'
urlpatterns = [
    path('post/create/', views.create_match_post, name='create_match_post'),  # 作成
    path('post/edit/<int:post_id>/', views.edit_match_post, name='edit_match_post'),  # 修正
    path('post/', views.read_post, name='read_post'),   # 一覧表示
    path('post/delete/<int:post_id>/', views.delete_match_post, name='delete_match_post'),   # 削除
    path('', views.create_user, name='create_user'),
    path('post/graph/', views.match_graph, name='match_graph')
]