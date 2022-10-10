from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
                #posts/ > GET(list), POST(create)
                #posts/id/ > GET(retrieve), PUT/PATCH(update), DELETE

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.CategoryListView.as_view()), # 8000/categories/

    path('comments/', views.CommentListCreateView.as_view()), # 8000/comments/
    path('comments/<int:pk>/', views.CommentDetailView.as_view()), # 8000/comments/<id>



    # path('likes/', views.LikeCreateView.as_view()),
    # path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
    
    # path('categories/', views.category_list), # 8000/categories/
    # path('categories1/', views.CategoryListView.as_view()), # 8000/categories1/
    # path('posts/', views.PostListCreateView.as_view()), # 8000/posts/
    # path('posts/<int:pk>/', views.PostDetailView.as_view()), # 8000/posts/<id>
]


# TODO likes
# TODO favorites
# TODO followers
