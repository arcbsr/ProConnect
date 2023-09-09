import googletrans
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.AIToolsModel import AITextSerializer, LanguageSerializer, TranslationSerializer
from rest_framework import status
from google.cloud import translate as translateN
from google.cloud import translate_v2 as translate
from rest_framework import generics, permissions
from django.http import JsonResponse
import requests
import time
import openai
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from googletrans import Translator

ALL_COUNTRY_DATA = [
    {"language_code": "af", "display_name": "Afrikaans"},
    {"language_code": "sq", "display_name": "Albanian"},
    {"language_code": "am", "display_name": "Amharic"},
    {"language_code": "ar", "display_name": "Arabic"},
    {"language_code": "hy", "display_name": "Armenian"},
    {"language_code": "as", "display_name": "Assamese"},
    {"language_code": "ay", "display_name": "Aymara"},
    {"language_code": "az", "display_name": "Azerbaijani"},
    {"language_code": "bm", "display_name": "Bambara"},
    {"language_code": "eu", "display_name": "Basque"},
    {"language_code": "be", "display_name": "Belarusian"},
    {"language_code": "bn", "display_name": "Bengali"},
    {"language_code": "bho", "display_name": "Bhojpuri"},
    {"language_code": "bs", "display_name": "Bosnian"},
    {"language_code": "bg", "display_name": "Bulgarian"},
    {"language_code": "ca", "display_name": "Catalan"},
    {"language_code": "ceb", "display_name": "Cebuano"},
    {"language_code": "ny", "display_name": "Chichewa"},
    {"language_code": "zh", "display_name": "Chinese (Simplified)"},
    {"language_code": "zh-TW", "display_name": "Chinese (Traditional)"},
    {"language_code": "co", "display_name": "Corsican"},
    {"language_code": "hr", "display_name": "Croatian"},
    {"language_code": "cs", "display_name": "Czech"},
    {"language_code": "da", "display_name": "Danish"},
    {"language_code": "dv", "display_name": "Divehi"},
    {"language_code": "doi", "display_name": "Dogri"},
    {"language_code": "nl", "display_name": "Dutch"},
    {"language_code": "en", "display_name": "English"},
    {"language_code": "eo", "display_name": "Esperanto"},
    {"language_code": "et", "display_name": "Estonian"},
    {"language_code": "ee", "display_name": "Ewe"},
    {"language_code": "tl", "display_name": "Filipino"},
    {"language_code": "fi", "display_name": "Finnish"},
    {"language_code": "fr", "display_name": "French"},
    {"language_code": "fy", "display_name": "Frisian"},
    {"language_code": "gl", "display_name": "Galician"},
    {"language_code": "lg", "display_name": "Ganda"},
    {"language_code": "ka", "display_name": "Georgian"},
    {"language_code": "de", "display_name": "German"},
    {"language_code": "el", "display_name": "Greek"},
    {"language_code": "gn", "display_name": "Guarani"},
    {"language_code": "gu", "display_name": "Gujarati"},
    {"language_code": "ht", "display_name": "Haitian Creole"},
    {"language_code": "ha", "display_name": "Hausa"},
    {"language_code": "haw", "display_name": "Hawaiian"},
    {"language_code": "iw", "display_name": "Hebrew"},
    {"language_code": "hi", "display_name": "Hindi"},
    {"language_code": "hmn", "display_name": "Hmong"},
    {"language_code": "hu", "display_name": "Hungarian"},
    {"language_code": "is", "display_name": "Icelandic"},
    {"language_code": "ig", "display_name": "Igbo"},
    {"language_code": "ilo", "display_name": "Iloko"},
    {"language_code": "id", "display_name": "Indonesian"},
    {"language_code": "ga", "display_name": "Irish Gaelic"},
    {"language_code": "it", "display_name": "Italian"},
    {"language_code": "ja", "display_name": "Japanese"},
    {"language_code": "jw", "display_name": "Javanese"},
    {"language_code": "kn", "display_name": "Kannada"},
    {"language_code": "kk", "display_name": "Kazakh"},
    {"language_code": "km", "display_name": "Khmer"},
    {"language_code": "rw", "display_name": "Kinyarwanda"},
    {"language_code": "gom", "display_name": "Konkani"},
    {"language_code": "ko", "display_name": "Korean"},
]

class TranslateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        serializer = TranslationSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            target_language = serializer.validated_data['target_language']

            # try:
            #     client = translateN.TranslationServiceClient()
            #     parent = client.location_path("proconnect-398414", "global")

            #     response = client.translate_text(
            #         parent=parent,
            #         contents=[text],
            #         target_language_code=target_language,
            #     )

            #     translated_text = response.translations[0].translated_text
            #     translated_text = text
            #     return Response({'translated_text': translated_texto})
            # except Exception as e:
            #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                translate_client = translate.Client()

                if isinstance(text, bytes):
                    text = text.decode("utf-8")

                # Text can also be a sequence of strings, in which case this method
                # will return a sequence of results for each text.
                result = translate_client.translate(text, target_language=target_language)

                print("Text: {}".format(result["input"]))
                print("Translation: {}".format(result["translatedText"]))
                print("Detected source language: {}".format(result["detectedSourceLanguage"]))
                return Response({'translated_text': result["translatedText"]})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LanguageListView(generics.ListAPIView):
        serializer_class = LanguageSerializer
        permission_classes = [permissions.IsAuthenticated]
        def list(self, request, *args, **kwargs):
            try:
                # client = translate.Client()
                # supported_languages = client.get_languages()

                # # Extract language codes and display names
                # languages_data = [{'language_code': lang['language'], 'display_name': lang['name']} for lang in supported_languages]

                # serializer = self.get_serializer(languages_data, many=True)
                # return Response(serializer.data)
                return JsonResponse({"languages": ALL_COUNTRY_DATA})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class AIPriceAssist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = '2d1446b9b1b20cbf498762b5fb48d081'
        city = self.kwargs.get('city')
        # lat = '51.5604885'
        # lon = '0.0756475'
        # timestamp = int(time.time())
        # # '1668487200'  # Replace with your desired timestamp
        
        # response = requests.get(f'http://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}&units=metric')
        # # print(f'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}')
        # # https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=51.5604885&lon=0.0756475&dt=1694191370&appid=2d1446b9b1b20cbf498762b5fb48d081&units=metric
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Adjust units as needed (metric, imperial, etc.)
        }
        # TODO: will remove on live mode...
        params = {
            "condition": 'rainy',
            "icon":   'http link will be sent',
            "price":   '120,110,130',
        }
        # End of dummy
        return JsonResponse(params)
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data['weather'][0]['main'])
            params = {
            "condition": data['weather'][0]['main'],
            "icon":   data['weather'][0]['icon'],
            "price":   '+10',
        }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)
    

class GenerateAIText(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AITextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            api_key = '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'
            openai.api_key =  api_key
            # os.getenv("OPENAI_API_KEY")
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
            expert_reply = chat_completion['choices'][0]['message']['content']
            # expert_reply = 'Dummy text'
            if expert_reply:
                return JsonResponse({'expertsays': expert_reply})
            else:
                return JsonResponse({'error': 'Unable to fetch data'}, status=500)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


