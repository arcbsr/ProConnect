from django.urls import path, include
from api.models.Permissions import IsEmployer
from api.views import UserProfileViewSet, ProfileView, RegisterAPI,LoginAPI, UserProfileViewSet,CategoryList, login,JobViewSet, JobListAPI, JobSearchListAPI, JobDescriptionUpdateView

from rest_framework import routers
from knox import views as knox_views
from rest_framework import permissions
from api.views.AITools import CVAnalysisView, CVUploadView, GenerateAIText, TranslateAPIView, LanguageListView, AIPriceAssist
from api.views.JobDescriptionView import BidListCreateView, BidListCombineView, BiddingConfirmedView, BookmarkListCreateView, JobTypeList, MYBidListAPI, MYJobListAPI, PaymentView

from api.views.UserProfileView import UserViewSet

router = routers.DefaultRouter(trailing_slash=True)
# router.register('profile', UserProfileViewSet, basename='usersprofile_api')
router.register('jobs', JobViewSet)
router.register('users', UserViewSet)
# router.register('cv/upload', CVUploadView)
# router.register('bidding', BidListCreateView)



urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view()),
    path('joblist/', JobListAPI.as_view(), name='employer-jobs-list'),
    path('myjobs/', MYJobListAPI.as_view(), name='my-jobs-list'),
    path('mybids/', MYBidListAPI.as_view(), name='my-bids-list'),
    path('job/category/', CategoryList.as_view(), name='job-cat-list'),
    path('job/type/', JobTypeList.as_view(), name='job-cat-list'),
    path('joblist/<int:pk>/update/', JobDescriptionUpdateView.as_view(), name='job-update'),
    path('jobsearch/', JobSearchListAPI.as_view(), name='employer-jobs-list'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('job/<int:job_id>/bid/', BidListCreateView.as_view(), name='task-detail'),
    path('job/bidconfirmed/<int:bid_id>/', BiddingConfirmedView.as_view(), name='task-detail'),
    path('job/detail/<int:job_id>/', BidListCombineView.as_view(), name='test'),
    path('translate/', TranslateAPIView.as_view(), name='translate_api'),
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('weather/', AIPriceAssist.as_view(), name='get-weather'),
    path('aigenaratd/', GenerateAIText.as_view(), name='get-aitext'),
    path('job/<int:job_id>/bookmark/', BookmarkListCreateView.as_view(), name='task-bookmark'),
    path('makepayment/', PaymentView.as_view(), name='get-aitext'),
    path('cv/upload/', CVUploadView.as_view(), name='cv-upload'),
    path('cv/analysis/<int:pk>/', CVAnalysisView.as_view(), name='cv-analysis'),
    # path('job/', JobViewSet.as_view(), name='job'),
    # path('', include(router.urls)),

]