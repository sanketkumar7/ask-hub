from django.urls import path
from .views import *
urlpatterns = [
    path('',home_page,name='home'),
    path('login-user/',login_user,name='login_user'),
    path('register-user/',register_user,name='register_user'),
    path('logout-user/',logout_user,name='logout_user'),
    path('post-answer/<str:id>',post_answer,name='post_answer'),
    path('my-questions/',user_questions,name='user_questions'),
    path('delete-question/<str:id>',delete_question,name='delete_question'),
    # ajax requests
    path('like-unlike/<str:id>',like_unlike,name='like_unlike'),
]
