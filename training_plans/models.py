from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum
from multiselectfield import MultiSelectField
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
import datetime
from collections import defaultdict
from django.contrib.postgres.fields import ArrayField
from embed_video.fields import EmbedVideoField
from account.models import Member


class CustomRatingManager(models.Manager):
    use_for_related_fields = True

    def fGetVotesSum(self):
        return len(self.get_queryset())

    def fGetRatingResult(self):
        iResult, iCount = 0, 0

        for rating in self.all():
            iResult += rating.rating
            iCount = 1 + iCount
        if iCount == 0:
            return [iCount, 3]
        return [iCount, round(iResult/iCount)]


class CustomRating(models.Model):
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=3)
    member = models.ForeignKey(
        Member, verbose_name='voter', on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,  null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True,)  # id of related object
    # uses automatic content_type and object_id to create polymorphic relationships
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = CustomRatingManager()


class Equipment(models.Model):
    equipment = models.CharField(blank=True, null=True, max_length=40)

    KIND_CHOICES = (
        ('indoor', 'Indoor Geräte'),
        ('outdoor', 'Outdoor Geräte'),
        ('light', 'Leichte Geräte'),
    )

    kind = models.CharField(choices=KIND_CHOICES, blank=True,
                            null=True, default='indoor', max_length=40)

    def __str__(self):
        return self.equipment

    def fGetKindString(self):
        sHelp_string = self.kind
        dHelp_dictionairy = dict(self.KIND_CHOICES)
        return dHelp_dictionairy[sHelp_string]


class MuscleGroup(models.Model):
    title = models.CharField(blank=True, null=True, max_length=40)
    image = models.ImageField(
        upload_to='images/exercise_areas/', blank=True, null=True)
    identify = models.CharField(blank=True, null=True, max_length=40)
    benefit = models.PositiveSmallIntegerField(null=True, blank=True, default=2)
    def slug(self):
        return slugify(self.title)

    def __str__(self):
        return self.title

class Muscle(models.Model):
    title = models.CharField(blank=True, null=True, max_length=40)
    image = models.ImageField(
        upload_to='images/exercise_muscles/', blank=True, null=True)
    identify = models.CharField(blank=True, null=True, max_length=40)
    muscle_group = models.ForeignKey(MuscleGroup, related_name='muscles',
                             on_delete=models.CASCADE, null=True, blank=True)

    def slug(self):
        return slugify(self.title)

    def __str__(self):
        return self.title
    #MUSCLE_CHOICES = (
    #    ('vordere_schulter', 'vordere Schulter'),
    #    ('hintere_schulter', 'hintere Schulter'),
    #    ('seitliche_schulter', 'seitliche Schulter'),
#
    #    ('bizeps', 'Bizeps'),
    #    ('unterarme', 'Unterarme'),
    #    ('trizeps', 'Trizeps'),
#
    #    ('obere_brust', 'obere Brust'),
    #    ('mittlere_brust', 'mittlere Brust'),
    #    ('untere_brust', 'untere Brust'),
#
    #    ('seitlicher_bauch', 'seitlicher Bauch'),
    #    ('mittlere_bauch', 'mittlerer Bauch'),
#
    #    ('adduktoren', 'Adduktoren'),
    #    ('oberschenkel', 'Oberschenkel'),
    #    ('schienbein', 'Schienbein'),
    #    ('beinbizeps', 'Beinbizeps'),
    #    ('wade', 'Wade'),
#
    #    ('nacken', 'Nacken'),
    #    ('untergrätenmuskel', 'Untergrätenmuskel'),
    #    ('kapuzenmuskel', 'Kapuzenmuskel'),
    #    ('rautenmuskel', 'Rautenmuskel'),
    #    ('rundmuskel', 'Rundmuskel'),
    #    ('latissimus', 'Latissimus'),
    #    ('unterer_rücken', 'unterer Rücken'),
#
    #    ('po', 'Po')
    #)


class PossibleTrainingMuscleCombinations(models.Model):
    level = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    muscles = models.ManyToManyField(MuscleGroup, related_name='possible_training_groups', blank=True)
    muscles_count = models.PositiveIntegerField(null=True, blank=True, default=2)

    def IsNotEqual(self,oneCombination):
        for muscleGroup in oneCombination.muscles.all():
            if muscleGroup in self.muscles.all():
                return False
        return True


class Area(models.Model):
    area = models.CharField(blank=True, null=True, max_length=40)
    image = models.ImageField(
        upload_to='images/exercise_areas/', blank=True, null=True)
    identify = models.CharField(blank=True, null=True, max_length=40)

    def slug(self):
        return slugify(self.area)

    def __str__(self):
        return self.area


class Goal(models.Model):
    title = models.CharField(blank=True, null=True, max_length=40)
    identify = models.CharField(blank=True, null=True, max_length=40)
    image = models.ImageField(
        upload_to='images/training_goals/', blank=True, null=True)
    
    area_weak = models.BooleanField(default=True, blank=True, null=True)

    
    def slug(self):
        return slugify(self.title)

    def __str__(self):
        return self.title


class Kind(models.Model):
    kind = models.CharField(blank=True, null=True, max_length=40)
    image = models.ImageField(
        upload_to='images/exercise_kinds/', blank=True, null=True)
    identify = models.CharField(blank=True, null=True, max_length=40)

    def slug(self):
        return slugify(self.kind)

    def __str__(self):
        return self.kind


class Tipps(models.Model):
    tipp = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipp


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    kind = models.ManyToManyField(
        Kind, related_name='exercises', blank=True, default=None)
    equipment = models.ManyToManyField(
        Equipment, related_name='exercises', blank=True, default=None)
    tipps = models.ManyToManyField(
        Tipps, related_name='tipps', blank=True, default=None)
    title = models.CharField(max_length=200, blank=False, null=False)
    rating = GenericRelation(CustomRating, related_query_name='exercises')
    created = models.DateTimeField(default=timezone.now)
    start_weight = models.IntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)], default=20)
    efficiency = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=1)
    difficulty = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=1)
    video = EmbedVideoField(blank=True, null=True)
    cardio = models.BooleanField(default=False, blank=True, null=True)

    area = models.ForeignKey(Area, related_name='exercises',
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return self.title

    def slug(self):
        return slugify(self.title)

    def fGetKindString(self):
        return self.kind.values('identify')[0]['identify']

    def fGetAreaString(self):
        return self.area.area

    def save(self, *args, **kwargs):
        super(Exercise, self).save(*args, **kwargs)

    # get an evaluation of image rating
    # mayby for a ranking list
    def fGetRatingResult(self):
        return self.rating.fGetRatingResult()

    def fBoolEquipment(self):
        return len(self.equipment.all()) > 0


class Workout(models.Model):
    def ex_count(self):
        return str(self.exercises.count())

    def __str__(self):
        return ''

    def fGetExercises(self):
        return self.exercises.all().order_by('position')


class CoolDown(models.Model):
    def ex_count(self):
        return str(self.exercises.count())

    def __str__(self):
        return ''

    def fGetExercises(self):
        return self.exercises.all().order_by('position')


class WarmUp(models.Model):
    def ex_count(self):
        return str(self.exercises.count())

    def __str__(self):
        return ''

    def fGetExercises(self):
        return self.exercises.all().order_by('position')


class IncludedExercise(models.Model):
    exercise = models.ForeignKey(
        Exercise, related_name='used_siblings', on_delete=models.CASCADE, null=True)
    workout = models.ForeignKey(
        Workout, related_name='exercises', on_delete=models.CASCADE, blank=True, null=True)
    warm_up = models.ForeignKey(
        WarmUp, related_name='exercises', on_delete=models.CASCADE, blank=True, null=True)
    cool_down = models.ForeignKey(
        CoolDown, related_name='exercises', on_delete=models.CASCADE, blank=True, null=True)
    position = models.PositiveSmallIntegerField(
        null=True, blank=True, default=1)
    interval = models.BooleanField(default=False, blank=True, null=True)

    def fGetHighTime(self):
        iTime = 0
        sStatus = self.workout.training.plan.status
        if sStatus == '0':
            return datetime.timedelta(minutes=1)
        else:
            return datetime.timedelta(minutes=2)

    def fGetLowTime(self):
        iTime = 0
        sStatus = self.workout.training.plan.status
        if sStatus == '1':
            return datetime.timedelta(minutes=1)
        else:
            return datetime.timedelta(seconds=30)

    class Meta:
        ordering = ('position',)


class eMuscleBuilding(Exercise):
    muscle = models.ForeignKey(Muscle, related_name='main_from_exercises', blank=True, default=None, on_delete=models.CASCADE, null=True)
    sub_muscles = models.ManyToManyField(Muscle, related_name='exercises', blank=True,null=True)

    exercise_ptr = models.OneToOneField(
        Exercise, related_name='muscle_building', on_delete=models.CASCADE, parent_link=True)

    def fGetMuscleString(self):
        sHelp_string = self.muscle
        dHelp_dictionairy = dict(self.MUSCLE_CHOICES)
        return dHelp_dictionairy[sHelp_string]


class eEnduranceTraining(Exercise):
    exercise_ptr = models.OneToOneField(
        Exercise, related_name='endurance', on_delete=models.CASCADE, parent_link=True)


class eStretching(Exercise):
    exercise_ptr = models.OneToOneField(
        Exercise, related_name='stretching', on_delete=models.CASCADE, parent_link=True)


class Instruction(models.Model):
    step = models.TextField(blank=True)
    exercise = models.ForeignKey(
        Exercise, related_name='instruction', on_delete=models.CASCADE, blank=True, default=None)

    def __str__(self):
        return self.step


class Set(models.Model):
    weight = models.DecimalField(
        decimal_places=1, blank=True, max_digits=4, null=True, default=0)
    reversrements = models.SmallIntegerField(
        blank=True, null=True, default=12)  # Widerholungen
    exercise = models.ForeignKey(
        IncludedExercise, related_name='sets', blank=True, default=None, on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(null=True)
    duration = models.DurationField(
        blank=True, default=datetime.timedelta(minutes=10), null=True)

    class Meta:
        ordering = ('position',)

    def delete(self, *args, **kwargs):
        ret = super(Set, self).delete(*args, **kwargs)
        return ret


class Training_plan(models.Model):
    owner = models.ForeignKey(
        Member, related_name='training_plans_created', on_delete=models.CASCADE, null=True)
    is_finished = models.BooleanField(default=False)
    needed_equipment = models.ManyToManyField(
        Equipment, related_name='training_plans', blank=True)

    def fGetExerciseKindsList(self):
        return Kind.objects.all()
    exercise_kinds = models.ManyToManyField(
        Kind, related_name='training_plans', blank=True, default=fGetExerciseKindsList)
    title = models.CharField(
        max_length=200, blank=True, null=True, default=None)
    days = models.IntegerField(
        validators=[MaxValueValidator(365), MinValueValidator(1)], default=1)
    overview = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    favorite_from = models.ManyToManyField(
        Member, related_name='favorite_plans', blank=True)
    FREQUENZ_CHOICES = (
        ('daily', 'Tag'),
        ('weekly', 'Woche'),
        ('monthly', 'Monat'),
        ('yearly', 'Jahr'),
    )
    frequenz_number = models.IntegerField(
        validators=[MaxValueValidator(365), MinValueValidator(1)], default=1)
    frequenz = models.CharField(
        max_length=80, choices=FREQUENZ_CHOICES, blank=False, null=False, default='weekly')
    excluded_equipment = models.ManyToManyField(
        Equipment, related_name='training_plans_without', blank=True)

    STATUS_CHOICES = (
        ('0', _('Anfänger')),
        ('1', _('Erfahren')),
        ('2', _('Profi')),
    )
    status = models.CharField(
        max_length=80, choices=STATUS_CHOICES, blank=True, null=True, default='1')
    GENDER_CHOICES = (
        ('M', _('Männlich')),
        ('F', _('Weiblich')),
    )
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, blank=True, null=True)

    def slug(self):
        return slugify(self.title)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.title:
            return str(self.title)
        else:
            return 'hallo'

    def GetSortedGoalsCount(self):
        result = []
        trainings = self.trainings.all()
        for goal in Goal.objects.all():
            result.append([trainings.filter(goal=goal).count(), goal])
        result = sorted(result, key=lambda x: int(x[0]), reverse=True)
        return result

    def GetMainUsedGoals(self):
        goals = self.GetSortedGoalsCount()
        return goals[0:2]

    def fGetTrainingPlanDays(self):
        data = {}
        count = 1
        for training in self.trainings.all():
            if str(training.day) in data:
                data[str(training.day)][0].append(training.id)
                data[str(training.day)][1].append(training)
                data[str(training.day)][2] += 1
            else:
                data.update({str(training.day): [[training.id], [
                            training], 0]})
        keys = list(data.keys())
        keys.sort()
        dTrainings = {}
        for key in keys:
            dTrainings[key] = data[key]

        return dTrainings

    def fGetTrainingPlanDaysWithIds(self):
        data = {}
        count = 1
        for training in self.trainings.all():
            if training.day in data:
                data[training.day].append(training.id)
            else:
                data.update({training.day: [training.id]})
        keys = list(data.keys())
        keys.sort()
        dTrainings = {}
        for key in keys:
            dTrainings[key] = data[key]

        return dTrainings

    def fGetFrequenze(self):
        lTrainings = self.trainings.all()
        
        iTrainings_count = len(lTrainings)
        if iTrainings_count != 0:
            iFrequenze = int(lTrainings[iTrainings_count-1].day)
            print(iFrequenze)
            iMonth = None
            iWeeks = None
            iDays = None
            if iFrequenze >= 30:
                iMonth = int(iFrequenze / 30)
                iRemainder = iFrequenze % 30
                if iRemainder >= 7:
                    iWeeks = int(iRemainder / 7)
                    iDays = iRemainder % 7
                else:
                    iDays = iRemainder

            elif iFrequenze >= 7:
                iWeeks = int(iFrequenze / 7)
                iDays = iFrequenze % 7
            else:
                iDays = iFrequenze

            sResult = ''
            if iMonth:
                sMonth = _('Monate') if iMonth > 1 else _('Monat')
                sResult = str(iMonth) + ' ' + sMonth
            if iWeeks:
                sWeeks = _('Wochen') if iWeeks > 1 else _('Woche')
                sResult += (', ' if iMonth else '') + str(iWeeks) + ' ' + sWeeks
            if iDays > 0:
                sDays = _('Tage') if iDays > 1 else _('Tag')
                sResult += (', ' if iWeeks or iMonth else '') + \
                    str(iDays) + ' ' + sDays
            return sResult

    def fGetSortedEquipment(self):
        dData = {'light': [], 'indoor': [], 'outdoor': []}
        for e in self.needed_equipment.all():

            dData[e.kind].append(e)
        lDel = []
        for key in dData:
            if len(dData[key]) == 0:
                lDel.append(key)

        for var in lDel:
            del dData[var]

        return dData


class Training(models.Model):
    duration = models.DurationField(
        blank=True, default=datetime.timedelta(minutes=10))
    muscle_groups = models.ManyToManyField(MuscleGroup, related_name='trainings', blank=True)
    workout = models.OneToOneField(
        Workout, related_name='training', on_delete=models.CASCADE, blank=True, null=True)
    warm_up = models.OneToOneField(
        WarmUp, related_name='training', on_delete=models.CASCADE, blank=True, null=True)
    cool_down = models.OneToOneField(
        CoolDown, related_name='training', on_delete=models.CASCADE, blank=True, null=True)
    day = models.IntegerField(validators=[MaxValueValidator(
        365), MinValueValidator(1)], default=1, blank=True, null=True)
    unit = models.IntegerField(validators=[MaxValueValidator(
        365), MinValueValidator(1)], default=1, blank=True, null=True)
    title = models.CharField(
        max_length=200, blank=True, null=True, default=None)
    plan = models.ForeignKey(
        Training_plan, related_name='trainings', on_delete=models.CASCADE, blank=True, null=True)

    goal = models.ForeignKey(Goal, related_name='trainings',
                             on_delete=models.CASCADE, blank=True, null=True)

    areas_list = ArrayField(ArrayField(models.CharField(
        max_length=25, blank=True, null=True, default=None), size=2,), size=7, blank=True, null=True, default=None)
    workout_areas_list = ArrayField(ArrayField(models.CharField(
        max_length=25, blank=True, null=True, default=None), size=2,), size=7, blank=True, null=True, default=None)
    muscles_list = ArrayField(ArrayField(models.CharField(
        max_length=25, blank=True, null=True, default=None), size=2,), size=7, blank=True, null=True, default=None)
    workout_muscles_list = ArrayField(ArrayField(models.CharField(
        max_length=25, blank=True, null=True, default=None), size=2,), size=7, blank=True, null=True, default=None)
    def GetMainTrainedPartString(self):
        result = ''
        for i in range(2):
            area = self.areas_list[i]
            result += area[1] + ': ' + str(area[0]) + (', ' if i == 0 else '')

        return result

    def AddOrRemoveExerciseAreasList(self, exercise, intNumber):
        indexOfChangedAreaCounter = self.ChangeAreasListValue(exercise,intNumber,False)
        changedArea = self.areas_list[indexOfChangedAreaCounter]

        # sort area again, maybe the order is changed
        self.areas_list = sorted(self.areas_list, key=lambda x: int(x[0]), reverse=True)
        self.save()

        return self.CheckifAreasOrderOrValueChanged(changedArea,indexOfChangedAreaCounter)

    def AddOrRemoveExerciseMusclesList(self, exercise, intNumber):
        if exercise.exercise.muscle_building:   # if added exercise is muscle building
            indexOfChangedMuscleCounter = self.ChangeMusclesListValue(exercise,intNumber,False)
            changedMuscle = self.muscles_list[indexOfChangedMuscleCounter]

            # sort area again, maybe the order is changed
            self.muscles_list = sorted(self.muscles_list, key=lambda x: int(x[0]), reverse=True)
            self.save()

            return self.CheckifMusclesOrderOrValueChanged(changedMuscle,indexOfChangedMuscleCounter)
        else:
            self.ChangeAreasListValue(exercise,intNumber,False)
            return None   # no muscle building exercise was added

    def ChangeAreasListValue(self,exercise,intNumber,boolWorkout):
        if boolWorkout:
            for i in range(7):
                # area of added exercise
                if exercise.exercise.area.area == self.workout_areas_list[i][1]:
                    self.workout_areas_list[i][0] = int(int(self.workout_areas_list[i][0]) + intNumber)
                    return i
        else:
            for i in range(7):
                # area of added exercise
                if exercise.exercise.area.area == self.areas_list[i][1]:
                    self.areas_list[i][0] = int(int(self.areas_list[i][0]) + intNumber)
                    return i

    def ChangeMusclesListValue(self,exercise,intNumber,boolWorkout):
        if boolWorkout:
            for i in range(9):
                # area of added exercise
                if exercise.exercise.muscle_building.muscle.muscle_group.title == self.workout_muscles_list[i][1]:
                    self.workout_muscles_list[i][0] = int(int(self.workout_muscles_list[i][0]) + intNumber)
                    return i
        else:
            for i in range(9):
                # area of added exercise
                if exercise.exercise.muscle_building.muscle.muscle_group.title == self.muscles_list[i][1]:
                    self.muscles_list[i][0] = int(int(self.muscles_list[i][0]) + intNumber)
                    return i

    def AddOrRemoveExerciseWorkoutAreasList(self, exercise, intNumber):
        indexOfChangedAreaCounter = self.ChangeAreasListValue(exercise,intNumber,True)
        changedArea = self.workout_areas_list[indexOfChangedAreaCounter]
        # sort area again, maybe the order is changed
        self.workout_areas_list = sorted(self.workout_areas_list, key=lambda x: int(x[0]), reverse=True)
        self.save()

        return self.CheckifWorkoutAreasOrderChanged(changedArea,indexOfChangedAreaCounter)


    def AddOrRemoveExerciseWorkoutMusclesList(self, exercise, intNumber):
        if exercise.exercise.muscle_building:   # if added exercise is muscle building
            indexOfChangedMuscleCounter = self.ChangeMusclesListValue(exercise,intNumber,True)
            changedMuscle = self.workout_muscles_list[indexOfChangedMuscleCounter]

            # sort area again, maybe the order is changed
            self.workout_muscles_list = sorted(self.workout_muscles_list, key=lambda x: int(x[0]), reverse=True)
            self.save()

            return self.CheckifWorkoutMusclesOrderChanged(changedMuscle,indexOfChangedMuscleCounter)
        else:
            self.ChangeAreasListValue(exercise, intNumber,True)
            return None   # no muscle building exercise was added


    def CheckifMusclesOrderOrValueChanged(self,changedMuscle,indexOfChangedMuscleCounter):
        # if the order is changed, return new main areas
        if (changedMuscle != self.muscles_list[indexOfChangedMuscleCounter]):
            return ['changed_order', self.muscles_list[0:3]]
        else:
            return ['increased_value', [indexOfChangedMuscleCounter, self.muscles_list[indexOfChangedMuscleCounter][0]]]



    def CheckifAreasOrderOrValueChanged(self,changedArea,indexOfChangedAreaCounter):
        # if the order is changed, return new main areas
        if (changedArea != self.areas_list[indexOfChangedAreaCounter]):
            return ['changed_order', self.areas_list[0:3]]
        else:
            return ['increased_value', [indexOfChangedAreaCounter, self.areas_list[indexOfChangedAreaCounter][0]]]




    def CheckifWorkoutAreasOrderChanged(self,changedArea,indexOfChangedAreaCounter):
        # if the order is changed, return new main areas
        if (changedArea != self.workout_areas_list[indexOfChangedAreaCounter]) or (int(changedArea[0]) == 0):
            return ['changed_order', self.GetWorkoutAreasStrings()]
        else:
            return None  # if the order don't change return none

    def CheckifWorkoutMusclesOrderChanged(self,changedArea,indexOfChangedAreaCounter):
        # if the order is changed, return new main areas
        if (changedArea != self.workout_muscles_list[indexOfChangedAreaCounter]) or (int(changedArea[0]) == 0):
            return ['changed_order', self.GetWorkoutMusclesStrings()]
        else:
            return None  # if the order don't change return none

    def GetAllTrainingExercises(self):
        exercises = self.warm_up.fGetExercises()
        exercises = exercises | self.workout.fGetExercises()
        exercises = exercises | self.cool_down.fGetExercises()

        return exercises

    def GetMainTrainedPartSortedList(self, exercises):
        list = []
        lAreas = Area.objects.all()
        for area in lAreas:
            list.append(
                [exercises.filter(exercise__area=area).count(), area.area])
        list.sort(reverse=True)
        self.areas_list = list
        self.save()
        return list

    def GetMainTrainedMusclesSortedList(self, exercises):
        exercises = exercises.filter(exercise__kind__identify='muscle_building')
        list = []
        listMuscleGroups = MuscleGroup.objects.all()
        for group in listMuscleGroups:
            list.append(
                [exercises.filter(exercise__muscle_building__muscle__muscle_group__title=group.title).count(), group.title])
        list.sort(reverse=True)
        self.muscles_list = list
        self.save()
        return list

    def GetMainTrainedParts(self):
        if self.IsMuscleTraining():
            return self.GetMainTrainedMuscles()
        exercises = self.GetAllTrainingExercises()
        sorted_list = self.GetMainTrainedPartSortedList(exercises)

        return sorted_list[0:3]

    def GetMainTrainedMuscles(self):
        exercises = self.GetAllTrainingExercises()
        sorted_list = self.GetMainTrainedMusclesSortedList(exercises)

        return sorted_list[0:3]

    def IsMuscleTraining(self):
        if '0' or '1' or '2' in self.goal.identify:
            return True
        else:
            return False

    def GetMainTrainedWorkoutParts(self):
        if self.IsMuscleTraining():
            return self.GetMainTrainedWorkoutMuscles()
        exercises = self.workout.exercises.all()
        areas_list = self.GetMainTrainedPartSortedList(exercises)
        self.workout_areas_list = areas_list
        self.save()
        return self.GetWorkoutAreasStrings()

    def GetMainTrainedWorkoutMuscles(self):
        exercises = self.workout.exercises.all()
        areas_list = self.GetMainTrainedMusclesSortedList(exercises)
        self.workout_muscles_list = areas_list
        self.save()
        return self.GetWorkoutMusclesStrings()

    def GetWorkoutAreasStrings(self):
        areas_list = self.workout_areas_list[0:2]
        result = []
        for i in range(2):
            if int(areas_list[i][0]) != 0:
                result.append(areas_list[i][1])
            else:
                result.append('')
        return result

    def GetWorkoutMusclesStrings(self):
        muscles_list = self.workout_muscles_list[0:2]
        result = []
        for i in range(2):
            if int(muscles_list[i][0]) != 0:
                result.append(muscles_list[i][1])
            else:
                result.append('')
        return result

    def GetExercisesCount(self):
        return self.GetAllTrainingExercises().count()

    def GetKind(self):
        if self.goal:
            return self.goal.title
        else:
            return ''

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.unit) + '. Unit'


class CurrentPlan(models.Model):
    member = models.OneToOneField(
        Member, related_name='current_plan', on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(
        Training_plan, related_name='current_plans', on_delete=models.CASCADE, blank=True, null=True)
    begin = models.DateTimeField(default=timezone.now)

    def RemovePlan(self):
        self.plan = None

    def SetNewPlan(self, sPlan_id):
        self.plan = Training_plan.objects.get(id=sPlan_id)
        self.begin = timezone.now()

    def GetRecentTraining(self):
        lTrainings = self.plan.trainings
        iLast_day = lTrainings.latest('day').day
        iUsed_day = (datetime.datetime.now().date() - self.begin.date()).days
        while iUsed_day > iLast_day:
            iUsed_day -= iLast_day
        oCurrent_training = lTrainings.filter(day__gte=iUsed_day)[0]
        return oCurrent_training
