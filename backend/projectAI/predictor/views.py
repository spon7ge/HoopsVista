from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionInputSerializer
import random  # This is just for the mock prediction, replace with your actual model

# Create your views here.

class PredictView(APIView):
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['Name']
            stat_type = serializer.validated_data['Stat_Type']
            line = serializer.validated_data['Line']

            # TODO: Replace this with your actual prediction model
            # This is just a mock prediction
            predicted_value = random.uniform(line - 5, line + 5)
            probability = random.uniform(0, 1)

            return Response({
                'predicted_probability': probability,
                'predicted_value': predicted_value
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
