from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from api.models import UserProfile 
from django.contrib.auth.models import User
from api.models.Image import ImageSerializer
from rest_framework import viewsets,permissions
from rest_framework import status
from rest_framework.response import Response



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source='role.name', read_only=True)
    # user_pic = serializers.CharField(source='images.image', read_only=True)
    # profile_image_url = serializers.SerializerMethodField()
    # user = UserSerializer(many=False)
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ('id', 'name','email','user_role','phone')
        
class UserProfileSerializerImage(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'name','email','phone','profile_image', 'profile_image_url','latitude','longitude','country','area']
        read_only_fields = ['phone']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None
    
# class ImageViewSet(viewsets.ModelViewSet):
#     queryset = Image.objects.all()
#     # queryset = queryset.filter(is_active=True)
#     # queryset = queryset.filter(author=2)
#     serializer_class = ImageSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializerImage
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     return self.http_method_not_allowed(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
    
    def update(self, request, pk, format=None):
        try:
            instance = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializerImage(instance, data=request.data)

            # Check if the user making the request is the author of the instance
            if instance.user != request.user:
                return Response({"error": "You are not authorized to edit this job description."}, status=status.HTTP_403_FORBIDDEN)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "JobDescription not found"}, status=status.HTTP_404_NOT_FOUND)

class UserProfileViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = UserProfileSerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get_queryset(self):
        qs = UserProfile.objects.all()
        return qs
