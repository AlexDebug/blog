"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (PostListView, ListDetail, CreatePost, CreteComment, DeletePost,  DeleteComment,
                    UpdatePost, UpdateComment, like, dislike)

app_name = 'posts'

urlpatterns = [
    path('blog/', PostListView.as_view(), name='post'),
    path('blog/<pk>', ListDetail.as_view(), name='post_detail'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
    path('blog/<pk>/create_comment', CreteComment.as_view(), name='create_comment'),
    path('blog/<pk>/edit/delete', DeletePost.as_view(), name='delete_post'),
    path('comment/<pk>/edit/delete', DeleteComment.as_view(), name='delete_comment'),
    path('blog/<pk>/edit', UpdatePost.as_view(), name='update_post'),
    path('comment/<pk>/edit', UpdateComment.as_view(), name='update_comment'),
    path('blog/<pk>/like', like, name='like'),
    path('blog/<pk>/dislike', dislike, name='dislike'),
]
