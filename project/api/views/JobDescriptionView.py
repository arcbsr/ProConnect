
import os
import uuid
from rest_framework import serializers
from api.models import JobDescription, ProjectStatus
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from django.forms.models import model_to_dict
from rest_framework import generics, filters
from api.models.CVAnalyzerModel import CV
from api.models.Category import Category, Skills
from api.models.Category import Type
from api.models.ExtracKeyWord import KeywordExtractor
from api.models.JobBookmark import Bookmark
from api.models.OrderModel import Order, OrderSerializer, generate_unique_string
from api.models.Permissions import IsEmployer, IsOwner
from rest_framework.pagination import LimitOffsetPagination
from api.models.UserProfile import UserProfile
from api.models.JobBidding import Bidding, Review
from api.views.AITools import CVSerializer
from api.views.UserProfileView import UserProfileSerializer, UserSerializer
from rest_framework.exceptions import APIException
from rest_framework import status
from PyPDF2 import PdfReader
from project import settings


class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # You can specify the fields you want to include here

class CategoryList(generics.ListAPIView):

    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerialize

class JobTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'  # You can specify the fields you want to include here

class JobTypeList(generics.ListAPIView):

    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    queryset = Type.objects.all()
    serializer_class = JobTypeSerialize

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus.ProjectStatus
        fields = '__all__'

class JobDescriptionSerializer(serializers.ModelSerializer):
    
    # jobstatus = JobStatusSerializer()  # Serialize the related status field
    author_name = serializers.CharField(source='author.profile.name', read_only=True)
    author_role = serializers.CharField(source='author.profile.role.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    job_type_name = serializers.CharField(source='jobtype.name', read_only=True)
    job_status = serializers.CharField(source='jobstatus.name', read_only=True)
    class Meta:
        model = JobDescription
        # fields = '__all__'
        fields = '__all__'
        # exclude = ['keyword']
        read_only_fields = ['is_active','author','keyword','jobstatus']
        

class JobDescriptionViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def get(self, request):
        # user = request.user
        
            return Response({
                'response': 'sdsadjhsjdhsgj',
            })

class JobViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.filter(jobstatus__name='Active')
    # .select_related('author__profile')
    # queryset = queryset.filter(is_active=True)
    # queryset = queryset.filter(author=2)
    serializer_class = JobDescriptionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['keyword']
    pagination_class = LimitOffsetPagination
    permission_classes = []
    
    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':# Apply authentication only for the "POST" action
            permission_classes.append(IsEmployer(self, self.request))
        # return []  # No authentication for other actions
        elif self.action == 'update':  # Apply authentication only for the "PUT" action
            permission_classes.append(IsEmployer(self, self.request))
        elif self.action == 'delete':  # Apply authentication only for the "DELETE" action
            permission_classes.append(IsEmployer(self, self.request))
        elif self.action == 'list':
             permission_classes.append(IsEmployer(self, self.request))
        return permission_classes   # No authentication for other actions
    @action(detail=False, methods=['GET'])
    def custom_list(self, request):
        # Your custom logic to retrieve a list of jobs goes here.
        jobs = JobDescription.objects.filter(jobstatus__name='Active')
        serializer = self.get_serializer(jobs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, pk, format=None):
        try:
            instance = JobDescription.objects.get(pk=pk)
            keywords = KeywordExtractor().extract_keywords(self.request.POST.get('description', ''))
            if keywords:
                instance.keyword = keywords
            serializer = JobDescriptionSerializer(instance, data=request.data)

            # Check if the user making the request is the author of the instance
            if instance.author != request.user:
                return Response({"error": "You are not authorized to edit this job description."}, status=status.HTTP_403_FORBIDDEN)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobDescription.DoesNotExist:
            return Response({"error": "JobDescription not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk, format=None):
        try:
            instance = JobDescription.objects.get(pk=pk)

            # Check if the user making the request is the author of the instance
            if instance.author != request.user:
                return Response({"error": "You are not authorized to delete this job description."}, status=status.HTTP_403_FORBIDDEN)

            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JobDescription.DoesNotExist:
            return Response({"error": "JobDescription not found"}, status=status.HTTP_404_NOT_FOUND)
    # def perform_destroy(self, instance):
    #     # Set the is_active field to False instead of physically deleting the object
    #     instance.is_active = False
    #     instance.save()
        
    def perform_create(self, serializer):
        # input_string = "apple banana orange"
        # parts = input_string.split()  # Splitting the string by whitespace
        # result = ", ".join(parts) 
        keyword_extractor = KeywordExtractor()
        skills = list(Skills.objects.all())
        if skills:
                skills_list = []
                keyword_extractor = KeywordExtractor()
                for s in skills:
                    skills_list.append(s.name)
        keywords = keyword_extractor.extract_keywords_withstops_fromlist(self.request.POST.get('description', ''),skills_list)
                
        # keywords = keyword_extractor.extract_keywords(self.request.POST.get('description', ''))
        serializer.save(author=self.request.user, keyword=keywords, is_active=True)

class JobListAPI(APIView):
    permission_classes = []

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        # permission_classes.append(IsEmployer(self, self.request))
        return permission_classes

    def post(self, request, format=None):
        serializer = JobDescriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Create the new instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, format=None):
        try:
            instance = JobDescription.objects.get(pk=pk)
            serializer = JobDescriptionSerializer(instance)
            return Response(serializer.data)
        except JobDescription.DoesNotExist:
            return Response({"error": "JobDescription not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        job_descriptions = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(job_descriptions, many=True)
        return Response(serializer.data)
    
class JobSearchListAPI(generics.ListAPIView):
    queryset = JobDescription.objects.select_related('author__profile')
    serializer_class = JobDescriptionSerializer



class JobDescriptionUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            instance = JobDescription.objects.get(pk=pk)
            serializer = JobDescriptionSerializer(instance, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobDescription.DoesNotExist:
            return Response({"error": "JobDescription not found"}, status=status.HTTP_404_NOT_FOUND)
        

class BidSerializer(serializers.ModelSerializer):
    bidder_name = serializers.CharField(source='worker.profile.name', read_only=True)
    bidder_id = serializers.CharField(source='worker.profile.user_id', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    employer_name = serializers.CharField(source='job.author.profile.name', read_only=True)
    employer_id = serializers.CharField(source='job.author.profile.user_id', read_only=True)
    class Meta:
        model = Bidding
        fields = '__all__'
        # exclude = ['bid_amount']
        extra_kwargs = {
            'job': {'required': False},  # Make job field not required
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class BidListCombineView(APIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
         
        job_id = self.kwargs['job_id']
        job_details = JobDescription.objects.filter(id=job_id).first()
        job_details_serializer = JobDescriptionSerializer(job_details, many=False)
        if not job_details:
            return Response({"error": "item not found"}, status=status.HTTP_404_NOT_FOUND)
        bids = Bidding.objects.filter(job__id=job_id)
        payments=[]
        serializer_order = OrderSerializer()
        for bidding in bids:
            if bidding.is_confirmed:
                 if job_details.author.id == self.request.user.id:
                    payments = Order.objects.filter(job_bid =bidding)
                    
        serializer_order = OrderSerializer(payments, many=True)
        my_bids = Bidding.objects.filter(job__id=job_id, worker_id= self.request.user.id).first()
        bid_serializer = BidSerializer(bids, many=True)
        worker = UserProfile.objects.all()[:3]
        worker_serializer = UserProfileSerializer(worker, many=True)
        skills = list(Skills.objects.all())
        # skill_serializer = SkillSerializer(skills[0], many = True)
        required_skills_list = []
        missing_skills_list = []
        missing_skills_obj=[]
        if skills:
            skills_list = []
            keyword_extractor = KeywordExtractor()
            for s in skills:
                skills_list.append(s.name)
            missing_skills_list =required_skills_list = keyword_extractor.extract_keywords_withstops_fromlist(job_details.description, skills_list)
            user_skills=[]
            my_cv = CV.objects.filter(user=self.request.user.id).first()
            if my_cv:
                absolute_path = os.path.join(settings.MEDIA_ROOT, my_cv.file.name)
                # print(absolute_path)
                if  os.path.exists(absolute_path):
                    # raise APIException("File not found", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    pdf_text = ""
                    with open(absolute_path, "rb") as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        for page_number, page in enumerate(pdf_reader.pages, start=1):
                            pdf_text += page.extract_text()

                    keyword_extractor = KeywordExtractor()

                    user_skills = keyword_extractor.extract_keywords_withstops_fromlist(pdf_text, required_skills_list)
                    # user_skills.append('cleaning')
                    for u_skill in user_skills:
                        missing_skills_list = [x for x in missing_skills_list if x.lower() != u_skill.lower()]

            for skill in skills:
                for mskill in missing_skills_list:
                    if skill.name.lower() == mskill.lower():
                        missing_skills_obj.append({
                            "name": skill.name,
                            "learn": skill.course_link
                        })
            print(required_skills_list)
            print(user_skills)
        AI_Price = []
        
        AI_Price.append({
            "price": 260,
            "weather": 'Cloudy',
            "details": "It's a weather details",
            "icon":"http://google.com/image.png"  # Adjust units as needed (metric, imperial, etc.)
        })
        
        if not my_bids:
            combined_data = {
            'detail' : job_details_serializer.data,
            'course_required' : missing_skills_obj,
            'bids': bid_serializer.data,
            'payments' : serializer_order.data,
            'recommended' : worker_serializer.data,
            'p_sug' : AI_Price,
             }
        else:
            my_bid_serializer = BidSerializer(my_bids, many=False)
            combined_data = {
                'detail' : job_details_serializer.data,
                'course_required' : missing_skills_obj,
                'bids': bid_serializer.data,
                'payments' : serializer_order.data,
                'my_bid': my_bid_serializer.data,
                'recommended' : worker_serializer.data,
                'p_sug' : AI_Price,
                 
            }

        return Response(combined_data)
    
class BidListCreateView(generics.ListCreateAPIView):
    # queryset = Bidding.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        biddings = Bidding.objects.filter(job__id=job_id)
        return  biddings

    # def list(self, request, *args, **kwargs):
    #     return self.http_method_not_allowed(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
       
        job = JobDescription.objects.get(pk=job_id)
        if job.author.id == self.request.user.id:
            return Response({"error": "You are not allow to bid in your own project."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)
    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']
       
        job = JobDescription.objects.get(pk=job_id)
        worker_id = self.request.user.id
        existing_bid = Bidding.objects.filter(job=job, worker_id=worker_id).first()

        if existing_bid:
            # Update existing bid
            serializer.update(existing_bid, serializer.validated_data)
        else:
            # Create new bid
            serializer.save(job=job, worker_id=worker_id)


class MYJobListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
            job_descriptions = JobDescription.objects.filter(author= self.request.user.id)
            serializer = JobDescriptionSerializer(job_descriptions, many=True)
            return Response(serializer.data)
    
        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MYBidListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
            job_descriptions = Bidding.objects.filter(worker= self.request.user.id)
            serializer = BidSerializer(job_descriptions, many=True)
            return Response(serializer.data)
    
        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BookmarkSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_description = serializers.CharField(source='job.description', read_only=True)
    class Meta:
        model = Bookmark
        fields = '__all__'
        # exclude = ['bid_amount']
        extra_kwargs = {
            'user': {'required': False},
            'job': {'required': False},  # Make job field not required
        }
class BookmarkListCreateView(generics.ListCreateAPIView):

    # queryset = Bidding.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        biddings = Bookmark.objects.filter(user__id=self.request.user.id)
        return  biddings

    # def list(self, request, *args, **kwargs):
    #     return self.http_method_not_allowed(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
        job = JobDescription.objects.get(pk=job_id)
        if not job:
            return Response({'error': 'No item found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']
       
        job = JobDescription.objects.get(pk=job_id)
        if not job:
            return Response({'error': 'No item found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_id = self.request.user.id
        existing_bookmark = Bookmark.objects.filter(job=job, user=self.request.user).first()

        if existing_bookmark:
            # print('Exist...')
            # Update existing bid
            # serializer.update(existing_bookmark, serializer.validated_data)
            # raise APIException("Item already bookmarked.", code=400)
            existing_bookmark.delete()
        else:
            # Create new bid
            serializer.save(job=job, user= self.request.user)

class BiddingConfirmedSerializer(serializers.ModelSerializer):
    bidder_name = serializers.CharField(source='worker.profile.name', read_only=True)
    bidder_id = serializers.CharField(source='worker.profile.user_id', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    employer_name = serializers.CharField(source='job.author.profile.name', read_only=True)
    employer_id = serializers.CharField(source='job.author.profile.user_id', read_only=True)
    class Meta:
        model = Bidding
        fields = '__all__'
        # exclude = ['bid_amount']
        extra_kwargs = {
            'job': {'required': False},
            'bid_amount': {'required': False},  # Make job field not required
        }
class BiddingConfirmedView(generics.ListCreateAPIView):

    # queryset = Bidding.objects.all()
    serializer_class = BiddingConfirmedSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        bid_id = self.kwargs['bid_id']
        bid = Bidding.objects.get(pk=bid_id)
        job = JobDescription.objects.get(pk=bid.job.id)
        if job.author.id != self.request.user.id:
            raise APIException("Permission invalid", code=status.HTTP_401_UNAUTHORIZED)
        if not job.is_active:
            message = 'Already acitive bid'
            raise APIException("Already active bid found", code=status.HTTP_400_BAD_REQUEST)
        bid.is_confirmed = True
        job.jobstatus = ProjectStatus.ProjectStatus.objects.get(name='On Progress')
        job.is_active = False
        job.save()
        serializer.update(bid, serializer.validated_data)
        message = 'Job created successfully.'
        return Response({'message': message}, status=status.HTTP_201_CREATED)

class ProjectCompletedView(generics.ListCreateAPIView):

    # queryset = Bidding.objects.all()
    serializer_class = BiddingConfirmedSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        bid_id = self.kwargs['bid_id']
        bid = Bidding.objects.get(pk=bid_id)
        job = JobDescription.objects.get(pk=bid.job.id)
        if job.author.id != self.request.user.id:
            raise APIException("Permission invalid", code=status.HTTP_401_UNAUTHORIZED)
        
        job.jobstatus = ProjectStatus.ProjectStatus.objects.get(name='Completed')
        job.is_active = False
        job.save()
        rating = self.request.POST.get('rating', None)
        if rating is None:
            rating = 10

        msg = self.request.POST.get('msg', None)
        if msg is None:
            msg = ''
        review = Review()
        review.job = job
        review.worker = bid.worker
        review.rate = rating
        review.message = msg

        existing_rating = Review.objects.filter(job=job).first()

        if existing_rating:
            # Update existing bid
            # review.update()
            Review.objects.filter(job=job,worker=bid.worker).delete()
        
            # Create new bid
        review.save()
        # serializer.update(bid, serializer.validated_data)
        message = 'Job is completed successfully.'
        return Response({'messagecsc': message}, status=status.HTTP_201_CREATED)

class PaymentView(generics.ListCreateAPIView):

    # queryset = Bidding.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            bid = serializer.validated_data['job_bid']
            amount = serializer.validated_data['total_amount']
            msg = serializer.validated_data['message']
            
            order = Order()
            order.order_number = uuid.uuid4().hex
            order.job_bid = bid
            order.total_amount = amount
            order.message = msg
            job = JobDescription.objects.get(pk=bid.job.id)
            if job.author.id != self.request.user.id:
                raise APIException("Permission invalid", code=status.HTTP_401_UNAUTHORIZED)
            if bid.is_confirmed:
                order.save()
                # if not instance:
                #     raise APIException("went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            else:
                raise APIException("worker id invalid", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            orders = Order.objects.filter(job_bid =bid )
            serializer_order = OrderSerializer(orders, many=True)
        return Response({'payments': serializer_order.data}, status=status.HTTP_201_CREATED)
    

