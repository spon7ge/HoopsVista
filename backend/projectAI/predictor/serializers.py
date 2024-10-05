from rest_framework import serializers

class PredictionInputSerializer(serializers.Serializer):
    Name = serializers.CharField(max_length=100)
    Stat_Type = serializers.CharField(max_length=50)
    Line = serializers.FloatField()
