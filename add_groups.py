from training_plans.models import MuscleGroup, PossibleTrainingMuscleCombinations
test = ['breast', 'trizeps']
groups = MuscleGroup.objects.all().exclude(identify__in=test)
important = MuscleGroup.objects.all().filter(identify__in=test)

for group in groups:
    new_ = PossibleTrainingMuscleCombinations.objects.create()
    new_.level = 2
    new_.muscles_count = 3
    new_.muscles.add(group)
    for newgroup in important:
        new_.muscles.add(newgroup)
    new_.save()
