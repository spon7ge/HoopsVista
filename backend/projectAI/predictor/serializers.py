from rest_framework import serializers

class PredictionInputSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Stat_Type = serializers.CharField()
    Line = serializers.FloatField()
    Sport = serializers.CharField(default='WNBA')
