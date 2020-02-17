from django.contrib import admin
from .models import Training, Exercise, Set, Instruction, Equipment, PossibleTrainingMuscleCombinations, MuscleGroup, Tipps, Muscle, eMuscleBuilding, Area, Goal, eEnduranceTraining, Kind, Training_plan, Workout, IncludedExercise, CoolDown, WarmUp, eStretching
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ['step']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'kind']


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ['kind', 'image']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['area']


@admin.register(PossibleTrainingMuscleCombinations)
class PossibleTrainingMuscleCombinationsAdmin(admin.ModelAdmin):
    list_display = ['level', 'GetMuscles']

    def GetMuscles(self, obj):
        return "\n".join([m.title for m in obj.muscles.all()])


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['title']
    exclude = ()


@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Tipps)
class TippsAdmin(admin.ModelAdmin):
    list_display = ['tipp']


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'weight', 'reversrements', 'duration']


class SetInline(admin.TabularInline):
    model = Set


class InstructionInline(admin.TabularInline):
    model = Instruction


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['title', 'image', 'get_kinds', 'area', 'video']

    def get_kinds(self, obj):
        return "\n".join([k.kind for k in obj.kind.all()])


@admin.register(eMuscleBuilding)
class eMuscleBuildingAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['title', 'area', 'get_equipmemts']
    inlines = [
        InstructionInline
    ]

    def get_equipmemts(self, obj):
        return "\n".join([e.equipment for e in obj.equipment.all()])


@admin.register(eStretching)
class eStretchingAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['title', 'area']
    inlines = [
        InstructionInline
    ]


@admin.register(eEnduranceTraining)
class eEnduranceTrainingAdmin(admin.ModelAdmin):
    exclude = ()
    inlines = [
        InstructionInline
    ]


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['__str__', 'warm_up_ex_count', ]

    def warm_up_ex_count(self, obj):
        print(dir(self))

        count = '0'
        if obj.warm_up:
            count = str(obj.warm_up.ex_count())
        return "WarmUp: {} Exercises".format(count)


# sub training nested
class SetInline(NestedStackedInline):
    model = Set
    extra = 0
    fk_name = 'exercise'


class IncluedeExerciseInline(NestedStackedInline):
    model = IncludedExercise
    extra = 0
    fields = ('exercise', 'position')
    inlines = [SetInline]
    sortable_field_name = "position"


class WorkoutAdmin(NestedModelAdmin):
    model = Workout
    readonly_fields = ('main_trained_part', 'id')
    inlines = [IncluedeExerciseInline]
    def main_trained_part(self, obj):

        return obj.main_trained_part()


class WarmUpAdmin(NestedModelAdmin):
    model = WarmUp
    inlines = [IncluedeExerciseInline]


class CoolDownAdmin(NestedModelAdmin):
    model = CoolDown
    inlines = [IncluedeExerciseInline]


admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WarmUp, WarmUpAdmin)
admin.site.register(CoolDown, CoolDownAdmin)
# #end sub training nested


@admin.register(IncludedExercise)
class IncludedExerciseAdmin(admin.ModelAdmin):
    inlines = (SetInline,)


class TrainingInline(admin.StackedInline):
    model = Training
    extra = 0
    exclude = ()
    list_display = ['__str__', 'warm_up_ex_count', ]
    fkname = 'training_plans'

    def warm_up_ex_count(self, obj):
        print(dir(self))

        count = '0'
        if obj.warm_up:
            count = str(obj.warm_up.ex_count())
        return "WarmUp: {} Exercises".format(count)


class Training_planAdmin(admin.ModelAdmin):
    model = Training_plan
    exclude = ()
    filter_horizontal = ('exercise_kinds', 'excluded_equipment')
    inlines = [TrainingInline]


admin.site.register(Training_plan, Training_planAdmin)
