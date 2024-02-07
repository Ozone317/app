from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', viewset=views.HelloViewSet, basename='Hello-viewset')
router.register('profile', viewset=views.UserProfileViewSet)
router.register('feed', viewset=views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]
