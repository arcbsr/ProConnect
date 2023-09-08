from rest_framework import serializers

class TranslationSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    target_language = serializers.CharField(max_length=5)


class LanguageSerializer(serializers.Serializer):
    language_code = serializers.CharField(max_length=5)
    display_name = serializers.CharField(max_length=50)

class AITextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)