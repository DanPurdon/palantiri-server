"""levelup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from palantiriAPI.views import register_user, login_user
from rest_framework import routers
from palantiriAPI.views import PostView, MessageView, CircleView, CommentView, InvitationView, CircleMemberView, CirclerView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'messages', MessageView, 'message')
router.register(r'posts', PostView, 'post')
router.register(r'circles', CircleView, 'circle')
router.register(r'comments', CommentView, 'comment')
router.register(r'invitations', InvitationView, 'invitation')
router.register(r'members', CircleMemberView, 'member')
router.register(r'circlers', CirclerView, 'circler')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
