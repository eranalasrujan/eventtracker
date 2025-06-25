from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration
    path('users/', views.user_list, name='user_list'),   # Admin-only: view user list

    # Login and logout using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='events:event_list'), name='logout'),
]
