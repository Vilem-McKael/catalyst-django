from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='posts_list_create'),
    path('posts/<int:post_id>/', views.PostRetrieveUpdateDeleteView.as_view(), name="post_detail"),
    path('posts/<int:collective_id>/get_posts', views.get_posts_by_collective, name="get_post_by_id"),
    path('collectives/', views.CollectiveListCreateView.as_view(), name='posts_list_create'),
    path('collectives/<int:collective_id>/', views.CollectiveRetrieveUpdateDeleteView.as_view(), name="post_detail"),
    path('collectives/search/', views.search_for_collective, name="collective_search"),
    path('collectives/join/', views.join_collective, name="join_collective"),
    path('collectives/user/', views.get_user_collectives, name="user_collectives"),
    path('comments/', views.PostListCreateView.as_view(), name='posts_list_create'),
    path('posts/<int:comment_id>/', views.PostRetrieveUpdateDeleteView.as_view(), name="post_detail"),
]