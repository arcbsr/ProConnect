
import json
import profile
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from api.models import UserProfile
from api.models.RoleModel import Role
from api.models.TokenRole import ExtendedAuthToken
from api.views import UserProfileSerializer
from response import ResponseSend
from django.forms.models import model_to_dict

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        profile: UserProfile = UserProfile()
        # profile.user_id = user
        profile.name = user.username
        profile.user = user
        profile.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user:
            raise serializers.ValidationError(
                'User not found.',
            )
        login(request, user)
        # return super(LoginAPI, self).post(request, format=None)

        profile = getProfileFromToken(request)
        # employer_role = Role.objects.get(id=1)
        # Role.objects.create(name='employer')
        token = AuthToken.objects.create(user)
        # token = ExtendedAuthToken.objects.create(user)
        # token.role = employer_role
        # token.save()
        if not token:
            raise serializers.ValidationError(
                'token is not generated...',
            )
        return Response(ResponseSend.sendMsg({
            'token': token[1],
            'profile': profile,

        }))
        # return Response({
        #             'token': token[1],
        #             'user': profile,

        #         }, )


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # user = request.user
        try:
            # data = UserProfile.objects.get(user_id = user.id)
            # # .select_related('profile')
            # if data:
            #     profile = UserProfileSerializer(data).data
            profile = getProfileFromToken(request)
            result = ResponseSend.sendMsg([profile])
            return Response({
                'response': result,
            })
        except Exception as e:
            raise serializers.ValidationError(
                e,
            )

    # def post(self, request):
    #     raise serializers.ValidationError(
    #             "post is not allowed",
    #         )
    # def delete(self, request, pk=None):
    #     raise serializers.ValidationError(
    #             "delete is not allowed",
    #         )
    # def put(self, request, pk=None):
    #     raise serializers.ValidationError(
    #             "put is not allowed",
    #         )


def getProfileFromToken(request):
    
    try:
        # return UserProfileSerializer(UserProfile.objects.get(user_id= request.user.id)).data
        return  model_to_dict(UserProfile.objects.get(user_id= request.user.id))
        
    except Exception as e:
        raise serializers.ValidationError(
                'Profile not found',)
             