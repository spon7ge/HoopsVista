from rest_framework import serializers

class PropSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    line = serializers.FloatField()
    odds = serializers.IntegerField()
    half = serializers.CharField(required=False, allow_null=True)

class PropCategorySerializer(serializers.Serializer):
    Points = serializers.ListField(child=PropSerializer(), required=False)
    Assists = serializers.ListField(child=PropSerializer(), required=False)
    Rebounds = serializers.ListField(child=PropSerializer(), required=False)
    Pts_Rebs = serializers.ListField(child=PropSerializer(), required=False)
    Pts_Asts = serializers.ListField(child=PropSerializer(), required=False)
    Rebs_Asts = serializers.ListField(child=PropSerializer(), required=False)
    Pts_Rebs_Asts = serializers.ListField(child=PropSerializer(), required=False)
    Three_PT_Made = serializers.ListField(child=PropSerializer(), required=False)

class PredictionInputSerializer(serializers.Serializer):
    player_name = serializers.CharField()
    stat_type = serializers.CharField()
    line = serializers.FloatField()
    sport = serializers.CharField(default='WNBA')
    date = serializers.DateField(required=False)

class PredictionOutputSerializer(serializers.Serializer):
    player_name = serializers.CharField()
    stat_type = serializers.CharField()
    line = serializers.FloatField()
    predicted_probability = serializers.FloatField()
    recommendation = serializers.CharField()
