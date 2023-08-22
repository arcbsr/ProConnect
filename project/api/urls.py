from django.urls import path, include
from api.views import UserProfileViewSet, ProfileView, RegisterAPI,LoginAPI, UserProfileViewSet, login
from rest_framework import routers
from knox import views as knox_views 
 

router = routers.DefaultRouter(trailing_slash=True)
# router.register('profile', UserProfileViewSet, basename='usersprofile_api')


urlpatterns = [
    path('', include(router.urls)), 
    path('profile/', ProfileView.as_view()),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),

]