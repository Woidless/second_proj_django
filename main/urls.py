from django.urls import path
from . import views


urlpatterns = [
    # path('categories/', views.category_list), # 8000/categories/
    # path('categories1/', views.CategoryListView.as_view()), # 8000/categories1/
    path('categories/', views.CategoryListView.as_view()), # 8000/categories/
    path('posts/', views.PostListCreateView.as_view()), # 8000/posts/
    path('posts/<int:pk>/', views.PostDetailView.as_view()), # 8000/posts/<id>
    path('comments/', views.CommentListCreateView.as_view()), # 8000/comments/
    path('comments/<int:pk>/', views.CommentDetailView.as_view()), # 8000/comments/<id>
]