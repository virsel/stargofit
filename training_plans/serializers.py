from rest_framework import serializers
from .models import Training_plan, Exercise


class Training_planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_plan
        fields = ('owner', 'exercise_kinds', 'excluded_equipment')


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        # for exercise title autocomplete
        fields = ('title', 'id')
