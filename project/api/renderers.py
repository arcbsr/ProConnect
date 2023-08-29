from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        wrapped_data = {'result': data}  # Wrap the data in a custom format
        return super().render(wrapped_data, accepted_media_type, renderer_context)