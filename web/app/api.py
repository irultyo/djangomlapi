from . import utils
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HomeView(APIView):
    def get(self, request):
        index = utils.api_patch_home()

        data = {
            "data": {
                "index": index
            }
        }
        return Response(data, status=status.HTTP_200_OK)

class RetrieveView(APIView):
    def post(self, request):
        index = request.data.get('index')
        patch_index = utils.api_retrieve(index)
        if index is not None:
            data = {
                "data": {
                    "index": patch_index  # Assuming this is the response data for any index
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index is required"}, status=status.HTTP_400_BAD_REQUEST)

class GenerateView(APIView):
    def post(self, request):
        patch_a = request.data.get('patch_a')
        patch_b = request.data.get('patch_b')
        model = request.data.get('model')
        
        images = {}
        for md in model:
            img = utils.generate_image(patch_a, patch_b, md)
            images[md] = img

        if patch_a is not None and patch_b is not None and model is not None:
            # For demonstration, assume a base64 string is returned
            data = {
                "data": {
                    "image": images
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "patch_a, patch_b, and model are required"}, status=status.HTTP_400_BAD_REQUEST)

