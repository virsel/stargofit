from django.core.management.base import BaseCommand
from training_plans.models import Instruction

class Command(BaseCommand):
    def handle(self, *args, **options):
        Instruction.objects.all().delete()