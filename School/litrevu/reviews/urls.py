from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/edit/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('review/create/<int:ticket_id>/', views.create_review, name='create_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('ticket-review/create/', views.create_ticket_review, name='create_ticket_review'),
    path('posts/', views.user_posts, name='user_posts'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('follow/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]