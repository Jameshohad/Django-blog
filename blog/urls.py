from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post-api')

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),

    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('api/v1/', include(router.urls)),

    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]