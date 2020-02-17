from modeltranslation.translator import translator, TranslationOptions
from training_plans.models import Exercise, Equipment, Instruction, Tipps, Area, MuscleGroup, Goal, Muscle, eMuscleBuilding, eEnduranceTraining, Kind, eStretching, Goal


class ExerciseTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Exercise, ExerciseTranslationOptions)


class eMuscleBuildingTranslationOptions(TranslationOptions):
    pass


translator.register(eMuscleBuilding, eMuscleBuildingTranslationOptions)


class eEnduranceTrainingTranslationOptions(TranslationOptions):
    pass


translator.register(eEnduranceTraining, eEnduranceTrainingTranslationOptions)


class eStretchingTranslationOptions(TranslationOptions):
    pass


translator.register(eStretching, eStretchingTranslationOptions)


class EquipmentTranslationOptions(TranslationOptions):
    fields = ('equipment',)


translator.register(Equipment, EquipmentTranslationOptions)


class KindTranslationOptions(TranslationOptions):
    fields = ('kind',)


translator.register(Kind, KindTranslationOptions)


class AreaTranslationOptions(TranslationOptions):
    fields = ('area',)


translator.register(Area, AreaTranslationOptions)


class GoalTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Goal, GoalTranslationOptions)


class MuscleGroupTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(MuscleGroup, MuscleGroupTranslationOptions)


class MuscleTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Muscle, MuscleTranslationOptions)


class InstructionTranslationOptions(TranslationOptions):
    fields = ('step',)


translator.register(Instruction, InstructionTranslationOptions)


class TippsTranslationOptions(TranslationOptions):
    fields = ('tipp',)


translator.register(Tipps, TippsTranslationOptions)
