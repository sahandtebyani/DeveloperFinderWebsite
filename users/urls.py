from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('user/<str:pk>', views.user_profile, name='user-profile'),
    path('account', views.user_account, name='account'),
    path('edit-account', views.edit_account, name='edit-account'),
    path('create-skill', views.create_skill, name='create-skill'),
    path('edit-skill/<str:pk>', views.edit_skill, name='edit-skill'),
    path('delete-skill/<str:pk>', views.delete_skill, name='delete-skill'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
