from rest_framework import serializers
from ..models import  Training_plan,  Exercise



class Training_planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_plan
        fields = []







