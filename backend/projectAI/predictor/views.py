from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import json
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_wnba_props(request):
    logger.info(f"Received request for WNBA props")
    json_file_path = os.path.join(settings.BASE_DIR, 'predictor', 'wnba_props.json')
    logger.info(f"Attempting to read file from: {json_file_path}")
    
    try:
        if not os.path.exists(json_file_path):
            logger.error(f"File not found: {json_file_path}")
            return Response({"error": "WNBA props data file not found"}, status=status.HTTP_404_NOT_FOUND)
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        logger.info("Successfully loaded WNBA props data")
        return Response(data)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return Response({"error": f"Invalid JSON data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)