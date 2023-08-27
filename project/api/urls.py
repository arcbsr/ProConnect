from django.urls import path, include
from api.models.Permissions import IsEmployer
from api.views import UserProfileViewSet, ProfileView, RegisterAPI,LoginAPI, UserProfileViewSet,CategoryList, login,JobViewSet, JobListAPI, JobSearchListAPI, JobDescriptionUpdateView

from rest_framework import routers
from knox import views as knox_views
from rest_framework import permissions
from api.views.JobDescriptionView import JobTypeList

from api.views.UserProfileView import UserViewSet

router = routers.DefaultRouter(trailing_slash=True)
# router.register('profile', UserProfileViewSet, basename='usersprofile_api')
router.register('jobs', JobViewSet)
router.register('users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view()),
    path('joblist/', JobListAPI.as_view(), name='employer-jobs-list'),
    path('job/category/', CategoryList.as_view(), name='job-cat-list'),
    path('job/type/', JobTypeList.as_view(), name='job-cat-list'),
    path('joblist/<int:pk>/update/', JobDescriptionUpdateView.as_view(), name='job-update'),
    path('jobsearch/', JobSearchListAPI.as_view(), name='employer-jobs-list'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('job/', JobViewSet.as_view(), name='job'),
    # path('', include(router.urls)),

]