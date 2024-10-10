from django.http import JsonResponse
from django.conf import settings
import os
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_wnba_props(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'predictor', 'wnba_props.json')
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return Response(data)
    except FileNotFoundError:
        return Response({"error": "WNBA props data not found"}, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Remove or update PropsView if it's no longer needed
# class PropsView(APIView):
#     def get(self, request):
#         # Update this method to work with JSON data if still needed
#         pass