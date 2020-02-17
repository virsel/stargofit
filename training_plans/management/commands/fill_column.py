from django.core.management.base import BaseCommand, CommandError
from training_plans.models import Exercise

class Command(BaseCommand):

    def handle(self, *args, **options):       
       exercises = Exercise.objects.all()
       id = 0
       for exercise in exercises:
            exercise.kind.kind_id = 1
            exercise.kind.exercise_id = id
            exercise.kind.id = 0
            id = id + 1
            exercise.save()