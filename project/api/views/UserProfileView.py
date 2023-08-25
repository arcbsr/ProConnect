from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from api.models import UserProfile 
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source='role.name', read_only=True)

    # user = UserSerializer(many=False)
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ('id', 'name','email','user_role','phone')


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
