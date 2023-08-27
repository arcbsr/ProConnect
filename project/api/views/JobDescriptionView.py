
from rest_framework import serializers
from api.models import JobDescription
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from django.forms.models import model_to_dict
from rest_framework import generics, filters
from api.models.Category import Category
from api.models.Category import Type
from api.models.Permissions import IsEmployer, IsOwner
from rest_framework.pagination import LimitOffsetPagination
from api.models.UserProfile import UserProfile
from api.views.UserProfileView import UserSerializer

from rest_framework import status


class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # You can specify the fields you want to include here

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize

class JobTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'  # You can specify the fields you want to include here

class JobTypeList(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = JobTypeSerialize

class JobDescriptionSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.profile.name', read_only=True)
    author_role = serializers.CharField(source='author.profile.role.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    job_type_name = serializers.CharField(source='jobtype.name', read_only=True)
    class Meta:
        model = JobDescription
        # fields = '__all__'
        fields = '__all__'
        # exclude = ['keyword']
        read_only_fields = ['is_active','author']

class JobDescriptionViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def get(self, request):
        # user = request.user
        
            return Response({
                'response': 'sdsadjhsjdhsgj',
            })

class JobViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
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
        print(self.action)
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, pk, format=None):
        try:
            instance = JobDescription.objects.get(pk=pk)
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
        input_string = "apple banana orange"
        parts = input_string.split()  # Splitting the string by whitespace
        result = ", ".join(parts) 
        serializer.save(author=self.request.user, keyword=result, is_active=True)

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