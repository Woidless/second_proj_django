from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view()), # 8000/accounts/
    path('<int:pk>/', views.UserDetailview.as_view()), # 8000/accounts/<id>/
    path('login/', views.CustomLoginView.as_view()), # 8000/accounts/login/
    path('logout/', views.CustomLogoutView.as_view()), # 8000/accounts/logout/
    path('register/', views.UserRegisterView.as_view()) # 8000/register/
]