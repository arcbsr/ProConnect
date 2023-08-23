from rest_framework import serializers
from api.models import JobDescription
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'


class JobDescriptionViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def get(self, request):
        # user = request.user
        
            return Response({
                'response': 'sdsadjhsjdhsgj',
            })