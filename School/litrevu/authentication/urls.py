from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # ← Cette ligne redirige vers login
]