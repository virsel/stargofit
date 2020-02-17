from training_plans.models import MuscleGroup, PossibleTrainingMuscleCombinations


class PossibleTrainingMuscleCombinationsFunctions():
    @staticmethod
    def AddCombinations(*args):
        listMainMuscleGroups = args[0]
        listElementAdditionalMuscleGroups = MuscleGroup.objects.all().exclude(
            identify__in=listMainMuscleGroups)
        listElementMainMuscleGroups = MuscleGroup.objects.all().filter(
            identify__in=listMainMuscleGroups)
        for additionalGroup in listElementAdditionalMuscleGroups:
            newCombination = PossibleTrainingMuscleCombinations.objects.create()
            newCombination.level = 2
            newCombination.muscles_count = len(listMainMuscleGroups) + 1
            newCombination.muscles.add(additionalGroup)
            for mainGroup in listElementMainMuscleGroups:
                newCombination.muscles.add(mainGroup)
            if not PossibleTrainingMuscleCombinationsFunctions.TestIfCombinationExists(newCombination):
                newCombination.save()

    @staticmethod
    def ConcatenateCombinations(*args):
        level = args[0]
        muscleCount = args[1]
        listBasisCombinations = PossibleTrainingMuscleCombinations.objects.all().filter(
            level=level).filter(muscles_count=muscleCount)
        for basisCombination in listBasisCombinations:
            listAdditionalCombinations = listBasisCombinations.exclude(
                id=basisCombination.id)
            for additionalCombination in listAdditionalCombinations:
                newCombination = PossibleTrainingMuscleCombinations.objects.create()
                newCombination.level = 1
                newCombination.muscles_count = muscleCount * 2

                for muscleGroup in additionalCombination.muscles.all():
                    newCombination.muscles.add(muscleGroup)
                for muscleGroup in basisCombination.muscles.all():
                    newCombination.muscles.add(muscleGroup)
                if not PossibleTrainingMuscleCombinationsFunctions.TestIfCombinationExists(newCombination):
                    newCombination.save()
                else:
                    newCombination.delete()

    @staticmethod
    def TestIfCombinationExists(newCombination):
        for existingCombination in PossibleTrainingMuscleCombinations.objects.all():
            if (set(newCombination.muscles.all()) == set(existingCombination.muscles.all())) and (newCombination.muscles_count == existingCombination.muscles_count):
                return True
            else:
                print(str(newCombination.muscles.all()) + ' already exists.')
                return False

    @staticmethod
    def Clean():
        for existingCombination in PossibleTrainingMuscleCombinations.objects.all():
            listRemainingCombinations = PossibleTrainingMuscleCombinations.objects.all(
            ).exclude(id=existingCombination.id)
            for remainingCombination in listRemainingCombinations:
                if (set(existingCombination.muscles.all()) == set(remainingCombination.muscles.all())) and (existingCombination.muscles_count == remainingCombination.muscles_count):
                    print('existing Combination: ' + str(existingCombination.muscles.all()
                                                         ) + ', must delete: ' + str(remainingCombination.muscles.all()))
                    remainingCombination.delete()
                else:
                    print(str(existingCombination.muscles.all()) + ', is exclusive')
