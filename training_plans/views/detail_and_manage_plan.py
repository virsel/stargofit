from django.shortcuts import render
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count, Q
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.template.defaultfilters import slugify
from django.core import serializers
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
import django

from braces.views import CsrfExemptMixin,JsonRequestResponseMixin
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.response import Response
import json
import math
import random
import redis
import datetime


from account.models import LikeDislike,Member
from ..models import Equipment, Training_plan, Kind, Area,Training, Goal, WarmUp,Workout,CoolDown, IncludedExercise, Set, CustomRating, CurrentPlan,Exercise, eEnduranceTraining, eMuscleBuilding,eStretching, MuscleGroup,PossibleTrainingMuscleCombinations
from .. import forms
from ..serializers import ExerciseSerializer
from .views import fFitnessStartPage

r = redis.Redis()


def GetRedisValue(stringKey):
    result = r.get(stringKey)
    return json.loads(result.decode('utf-8'))


def GetWeekCountOfMuscleTraining():
    listSortedTrainingGoalsOfAllDays = GetRedisValue('listSortedTrainingGoalsOfAllDays')

    iMuscle_count = listSortedTrainingGoalsOfAllDays.count('0')
    iStrength_count = listSortedTrainingGoalsOfAllDays.count('1')
    iDefinition_count = listSortedTrainingGoalsOfAllDays.count('2')
    iWeek_break = round(len(listSortedTrainingGoalsOfAllDays) / 7)

    dResult = {}
    if iMuscle_count > 0:
        iMuscle_count = round(iMuscle_count / iWeek_break) 
        dResult.update({'0':iMuscle_count})
        
    if iStrength_count > 0:
        iStrength_count = round(iStrength_count / iWeek_break) 
        dResult.update({'1':iStrength_count})
        
    if iDefinition_count > 0:
        iDefinition_count = round(iDefinition_count / iWeek_break) 
        dResult.update({'2':iDefinition_count})
    return dResult



# training duration control
def fSetTrainingDuration(iValue_seconds):
    iCurrant_value = r.get('training_duration')
    iCurrant_value = json.loads(iCurrant_value.decode('utf-8'))
    r.set('training_duration',iValue_seconds - iCurrant_value)





def RemoveSetFromExercise(objectSet):
    objectIncludedExercise = objectSet.exercise
    objectIncludedExercise.sets.remove(objectSet)
    objectIncludedExercise.save()
    objectSet.delete()

def AddSetToExercise(objectIncludedExercise,position,timedeltaDuration=None,intRepeats=None):
    new_set = Set.objects.create()
    new_set.position = position
    if timedeltaDuration != None:
        new_set.duration = timedeltaDuration
    if intRepeats != None:
        new_set.reversrements = intRepeats
    new_set.exercise = objectIncludedExercise
    objectIncludedExercise.sets.add(new_set)
    new_set.save()
    objectIncludedExercise.save()
    return new_set

# set
def SetRemainingTrainingDuration(iDuration_seconds,sKind):
    if sKind == 'muscle_building':
        fSetTrainingDuration(iDuration_seconds + 40)
    elif sKind == 'stretching':
        fSetTrainingDuration(iDuration_seconds + 20)
    else:
        fSetTrainingDuration(iDuration_seconds + 60)

# #end set


def AddNewExerciseToTraining(objectExercise,stringPos,objectTraining,stringMainKind,bIntervall = False):
    included_exercise = IncludedExercise.objects.create()
    included_exercise.exercise = objectExercise
    included_exercise.position = int(stringPos)

    if stringMainKind == 'warm':
        objectTraining.warm_up.exercises.add(included_exercise)
        objectTraining.warm_up.save()
    elif stringMainKind == 'train':
        objectTraining.workout.exercises.add(included_exercise)
        objectTraining.workout.save()
    else:
        objectTraining.cool_down.exercises.add(included_exercise)
        objectTraining.cool_down.save()
    AddNeededEquToPlan(objectTraining.plan,objectExercise)
    included_exercise.interval = bIntervall
    included_exercise.save()

    return included_exercise

# day List
def fGetUnitDayList(intFrequenz,iUnits):
    lDays = []
    iRemaining_units = iUnits
    iUnit_frequenz = 1
    for i in range(intFrequenz):
        if iRemaining_units != 0:
            iLeft_days = intFrequenz - i
            if iLeft_days < iRemaining_units:
                iUnits_per_day = round(iRemaining_units / iLeft_days)
                for u in range(iUnits_per_day):
                    lDays.append(i+1)
                    iRemaining_units -= 1
                    print(lDays)
            else:
                if not iRemaining_units == 1:

                    if iUnit_frequenz == 1:
                        iUnit_frequenz = math.ceil((iLeft_days-1) / (iRemaining_units-1))
                        lDays.append(i+1)
                        iRemaining_units -= 1

                    else:
                        iUnit_frequenz -= 1

                else:
                    if iLeft_days == 1:
                        lDays.append(i+1)
                        iRemaining_units -= 1
    return lDays
# #end day List


def Training_planGenerateFinish(request):
    
    dData = request.POST.get('data')
    dData = json.loads(dData)
    new_training_plan = CreateNewTrainingPlan(request.user,dData['title'])
    iUnits = int(dData['units'])
    lDuration = dData['time']
    lGoals = dData['goals']
    sStatus = dData['status']
    intFrequenz = int(dData['frequenz'])
    lPercentages = dData['goals_percentage']
    listSortedTrainingGoalsOfAllDays = GetSortedListOfTrainingGoals(lGoals,iUnits,lPercentages)

    lDays = fGetUnitDayList(intFrequenz,iUnits)
    DebugPrint('unit goals', listSortedTrainingGoalsOfAllDays)
    SetRedisStartDatabase()
    sDay = lDays[0]
    iUnit = 0
    for i in range(iUnits):
        sGoal = listSortedTrainingGoalsOfAllDays[i]
        new_training = AddNewTrainingToPlan(new_training_plan,lDays[i])
        SetTrainingGoal(new_training,sGoal)

    listTrainings = new_training_plan.trainings.all()
    SetMuscleTrainingSplits(listSortedTrainingGoalsOfAllDays,listTrainings)

    for i in range(iUnits):
        iDuration = fGetUnitDuration(lDuration,sGoal)
        DebugPrint('duration', iDuration)
        r.set('training_duration',iDuration * 60)
        new_training = listTrainings[i]

        GenerateWarmUpFromTraining(sGoal,iDuration,new_training)
        GenerateTrainingCoolDown(sGoal,new_training)
        GenerateTrainingWorkout(sGoal,new_training)
        new_training.save()


    new_training_plan.save()
    url = str(new_training_plan.id) + '/' + str(new_training_plan.slug()) + '/'   # redirect to detail view
    return JsonResponse({'url':url})



def SetMuscleTrainingSplits(listSortedTrainingGoalsOfAllDays,listTrainings):
    dictCountOfMuscleGoals = GetCountOfMuscleGoals(listSortedTrainingGoalsOfAllDays)
    iWeek_break = round(len(listSortedTrainingGoalsOfAllDays) / 7)

    if dictCountOfMuscleGoals['0'] > 0:
        intSplit = round(dictCountOfMuscleGoals['0'] / iWeek_break) 
        SetMuscleTrainingSplitOfOneGoal('0',intSplit,listTrainings)
    if dictCountOfMuscleGoals['1'] > 0:
        intSplit = round(dictCountOfMuscleGoals['1'] / iWeek_break) 
        SetMuscleTrainingSplitOfOneGoal('1',intSplit,listTrainings)
    if dictCountOfMuscleGoals['2'] > 0:
        intSplit = round(dictCountOfMuscleGoals['2'] / iWeek_break) 
        SetMuscleTrainingSplitOfOneGoal('2',intSplit,listTrainings)


def SetMuscleTrainingSplitOfOneGoal(stringGoal,intSplit,listTrainings):   # muscle building or strength or definition
    listOflistTrainingsMuscleGroups = GetSplittetTrainingsMuscleGroups(intSplit)
    listTrainings = listTrainings.filter(goal__identify=stringGoal)
    for i in range(intSplit):
        listTrainings[i].muscle_groups.set(list(listOflistTrainingsMuscleGroups[i].muscles.all()))
        listTrainings[i].save()
        print('training muscle groups: ')
        print(listTrainings[i].muscle_groups.all())



def GetSplittetTrainingsMuscleGroups(intSplit):
    intMusclesCount = round(9/intSplit)     # 8: number of different muscels
    result = []
    listMusclesExclude = []              # save muscles of each used combination
    for i in range(intSplit):
        if i == intSplit - 1:    # on last training try to use all remaining muscles
            listCombinations = PossibleTrainingMuscleCombinations.objects.exclude(muscles__in=listMusclesExclude).order_by('-muscles_count')
            intBiggestMusclesCount = listCombinations[0].muscles_count
            print('biggest count: ' + str(intBiggestMusclesCount))
            listCombinations = listCombinations.filter(muscles_count=intBiggestMusclesCount)
        else:   # normaly use combinations with muscles count equal to 9/SplitNumber
            listCombinations = PossibleTrainingMuscleCombinations.objects.exclude(muscles__in=listMusclesExclude)
            listCombinations = listCombinations.filter(muscles_count=intMusclesCount)
            if len(listCombinations) == 0:   # if no combination was founded search for combinations with +|- 1 muscles count
                listCombinations = listCombinations.filter(muscles_count__in=[intMusclesCount-1,intMusclesCount,intMusclesCount+1])
        oneCombination = random.sample(list(listCombinations),1)[0]
        result.append(oneCombination)
        listMusclesExclude.extend(list(oneCombination.muscles.all()))
    return result
        

def GetCountOfMuscleGoals(listSortedTrainingGoalsOfAllDays):
    goalCount = {'0' : 0, '1': 0, '2': 0}
    for goal in listSortedTrainingGoalsOfAllDays:
        if len(goal) > 1:    # days with more than one goal
            if '0' or '1' or '2' in goal:   # muscle building or strength or definition training
                goalCount['0'] += 1   # increase muscle building training
            elif '3' or '4' in goal:
                goalCount['3'] += 1     # increase goal count
        else:
            goalCount[str(goal)] +=1
    return goalCount


def GenerateWarmUpFromTraining(sGoal,iDuration,new_training):
    if  sGoal == '3' or sGoal == '4':  # endurance training - > stretch warm up
        iExercise_count = 10
        loExercises = Exercise.objects.filter(kind__identify='stretching')
        loExercises = random.sample(list(loExercises),iExercise_count)
        iEx_count = len(loExercises)
        for i in range(iEx_count):
            objectNewIncludedExercise = AddNewExerciseToTraining(loExercises[i],i+1,new_training,'warm')
            AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=40))
            SetRemainingTrainingDuration(40,'stretching')


    elif  sGoal == '0' or sGoal == '1' or sGoal == '2' or sGoal == '5':
        iWarm_up_duration = 15 if (iDuration > 60 and sGoal != '5') else (10 if sGoal != '5' else 5)
        loExercises = Exercise.objects.filter(cardio=True)
        e = random.sample(list(loExercises),1)[0]
        objectNewIncludedExercise = AddNewExerciseToTraining(e,1,new_training,'warm')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(minutes=iWarm_up_duration))
        SetRemainingTrainingDuration(iWarm_up_duration*60,'endurance')


def GenerateTrainingCoolDown(sGoal,objectTraining):

    if  sGoal == '0' or sGoal == '1' or sGoal == '2':
        lExercises = Exercise.objects.filter(cardio=True)
        exercise = random.sample(list(lExercises),1)[0]
        objectNewIncludedExercise = AddNewExerciseToTraining(exercise,1,objectTraining,'cool_down')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(minutes=8))
        SetRemainingTrainingDuration(8*60,'endurance')


    elif '5' != sGoal: # stretchin exercise -> no cool down
        iExercise_count = 8
        lExercises = list(Exercise.objects.filter(kind__identify='stretching'))
        random.shuffle(lExercises)
        for i in range(iExercise_count):
            exercise = lExercises[i]
            objectNewIncludedExercise = AddNewExerciseToTraining(exercise,i + 1,objectTraining,'cool_down')
            AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=30))
            SetRemainingTrainingDuration(30,'stretching')


def GenerateFatBurningWorkout(sGoal,objectTraining):
    iCase = random.randrange(0,7,1)
    # 0 -> Ausdauer Training 
    # 1 -> Kraft Training
    # 2 -> intervall
    if iCase == 0: 
        GenerateTrainingWorkout('3',objectTraining)
    elif iCase == 1:
        GenerateTrainingWorkout('1',objectTraining)
    elif iCase == 2:
        GenerateIntervalWorkout(objectTraining)



def GenerateIntervalWorkout(plan,workout):
    lExercises = Exercise.objects.filter(cardio=True)
    exercise = random.sample(list(lExercises),1)[0]
    iDuration_seconds = GetRedisValue('training_duration')
    if (iDuration_seconds / 60) > 30:
        objectNewIncludedExercise = AddNewExerciseToTraining(exercise,1,objectTraining,'train')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=iDuration_seconds - (25 * 60)))
        objectNewIncludedExercise = AddNewExerciseToTraining(exercise,2,objectTraining,'train')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=25 * 60))
    else:
        objectNewIncludedExercise = AddNewExerciseToTraining(exercise,1,objectTraining,'train')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=iDuration_seconds))

def GetMuscleExercisesOfTraining(intExerciseCount,listMuscleGroups):
    listExercises = []
    intExercisesPerGroup = intExerciseCount
    if len(listMuscleGroups) > 0:
        intExercisePerGroup = round(intExerciseCount / len(listMuscleGroups))
    print('get exercises for muscle group: ')
    print(listMuscleGroups)

    for i in range(len(listMuscleGroups)):
        listExercisesOfOneGroup = list(eMuscleBuilding.objects.filter(muscle__in=list(listMuscleGroups[i].muscles.all())))
        intSampleNumber = listMuscleGroups[i].benefit + intExercisePerGroup
        if listExercisesOfOneGroup:
            if len(listExercisesOfOneGroup) > intSampleNumber:
                listExercisesOfOneGroup = random.sample(listExercisesOfOneGroup,intSampleNumber)
            else:
                random.shuffle(listExercisesOfOneGroup)
            print('new list exercises: ' + str(listExercisesOfOneGroup))
            listExercises.extend(listExercisesOfOneGroup)

    return listExercises

def GenerateMuscleWorkout(sGoal,objectTraining):
    intExerciseCount = EstimateRemainingPossibleMuscleExerciseCount(GetMuscleExerciseSetRepeat(sGoal,0))
    print('remaining exercise count: ')
    print(intExerciseCount)
    lExercises = GetMuscleExercisesOfTraining(intExerciseCount,objectTraining.muscle_groups.all())


    for i in range(len(lExercises)):
        intRepeat = GetMuscleExerciseSetRepeat(sGoal,i)
        objectNewIncludedExercise = AddNewExerciseToTraining(lExercises[i],i+1,objectTraining,'train')
        intSetCount = random.randrange(3,5,1)
        AddMuscleSetsToExercise(intSetCount,objectNewIncludedExercise,intRepeat)



def GetMuscleExerciseSetRepeat(sGoal,intExercisePosition):
    if len(sGoal) == 1:     # one goal per day -> 
        return [10,14,12][int(sGoal)]   
    elif len(sGoal) == 2:
        if intExercisePosition % 2 == 0:    # on even number return repeats of first goal
            return [10,14,12][int(sGoal[0])]  
        else:
            return [10,14,12][int(sGoal[1])]  
    else: # three goals on one day
        if intExercisePosition % 3 == 0:    
            return [10,14,12][int(sGoal[0])]  
        elif intExercisePosition % 3 == 1:
            return [10,14,12][int(sGoal[1])]
        else:
            return [10,14,12][int(sGoal[2])]


def GenerateTrainingWorkout(sGoal,objectTraining):
    if '0' in sGoal or '1' in sGoal or '2' in sGoal: # muscle training 
        GenerateMuscleWorkout(sGoal,objectTraining)
    elif '4' in sGoal:
        GenerateFatBurningWorkout(sGoal,objectTraining)
    elif '3' in sGoal:
        GenerateEnduranceWorkout(objectTraining)
    else:
        GenerateAgilityWorkout(objectTraining)



def GenerateAgilityWorkout(objectTraining):
    intExerciseCount = GetRedisValue('training_duration') / 50
    lExercises = list(Exercise.objects.filter(kind__identify='stretching'))
    random.shuffle(lExercises)
    for i in range(intExerciseCount):
        exercise = lExercises[i]
        objectNewIncludedExercise = AddNewExerciseToTraining(exercise,i + 1,objectTraining,'train')
        AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=30))




def GenerateEnduranceWorkout(objectTraining):
    lExercises = Exercise.objects.filter(cardio=True)
    exercise = random.sample(list(lExercises),1)[0]
    objectNewIncludedExercise = AddNewExerciseToTraining(exercise,1,objectTraining,'train')
    AddSetToExercise(objectNewIncludedExercise,1,timedeltaDuration=datetime.timedelta(seconds=GetRedisValue('training_duration')))






def GetImportantMusclesInEachPlanInOneFrequenz():
    return ['breast', 'shoulder', 'trizeps', 'apdominal', 'legs', 'glutes','back','bizeps','underarms']

def GetSubMuscleStringsList(stringMuscle):
    pass



def fGetMuscleAreaCountList(iExercise,dExercise_count,iTraining_count):
    dResult = {}

    for key, value in dExercise_count.items():
        lList = dExercise_count[key]
        dResult.update({key:[]})
        for i in lList:
            dResult[key].append(round(iExercise * i * 0.1))

    return dResult




def GetExercisesForMuscleTraining(iExercises,listMuscleGroups):
    intCount = round(iExercises * (1/len(listMuscleGroups)))
    cache_exercises = []
    for i in range(len(listMuscleGroups)):
        muscleGroup = listMuscleGroups[i]
        lResult = list(eMuscleBuilding.objects.filter(muscle__in=muscleGroup.muscles.all()))
        if len(lResult) > intCount:
            lResult = lResult[:intCount]
        cache_exercises += lResult
    return cache_exercises




def EstimateRemainingPossibleMuscleExerciseCount(intRepeat):
    # estimate exercise count
    iLeft_seconds = GetRedisValue('training_duration')
    iOne_exercise_seconds = intRepeat * 3 * 4 + 4 * 40 + 60   # repeats, breaks between sets, break after exercise
    print('one exercise seconds : ' + str(iOne_exercise_seconds))
    return abs(round(iLeft_seconds / iOne_exercise_seconds))




def AddMuscleSetsToExercise(intSetCount,objectIncludedExercise,intStartRepeat):
    intExerciseDuration = 0
    for i in range(intSetCount):
        iRepeats = intStartRepeat - (2*i)
        AddSetToExercise(objectIncludedExercise,i+1,intRepeats=iRepeats)
        intExerciseDuration += iRepeats * 3 + 40
    intExerciseDuration += 90



def AddNeededEquToPlan(plan,exercise):
    if exercise.equipment.all():
        for e in exercise.equipment.all():
            plan.needed_equipment.add(e)
    plan.save()

def AddNewWarmUpToTraining(training):
    warm_up = WarmUp.objects.create()
    training.warm_up = warm_up
    warm_up.save()
    training.save()

def AddNewCoolDownToTraining(training):
    cool_down = CoolDown.objects.create()
    training.cool_down = cool_down
    cool_down.save()
    training.save()

def AddNewWorkoutToTraining(training):
    workout = Workout.objects.create()
    training.workout = workout
    workout.save()
    training.save()

def AddNewTrainingToPlan(plan,day=1):
    training = Training.objects.create()
    AddNewWarmUpToTraining(training)
    AddNewWorkoutToTraining(training)
    AddNewCoolDownToTraining(training)
    training.day = day
    training.save()
    plan.trainings.add(training)
    plan.save()
    return training


def CreateNewTrainingPlan(owner,title='neuer Plan'):
    plan = Training_plan.objects.create()
    plan.owner = owner
    plan.title = title
    plan.save()
    return plan

def CheckIfValidUser(request):
    return str(request.user) != 'AnonymousUser' 

def SetTrainingGoal(training,stringGoal):
    if len(stringGoal) > 1:
        if '0' or '1' or '2' in stringGoal:
            stringGoal = '0'
        elif '3' or '4' in stringGoal:
            stringGoal = '3'
    goal = Goal.objects.filter(identify=stringGoal)[0]
    training.goal = goal
    training.save()

def ChangeTrainingGoalRequest(request):
    value = str(request.POST.get('value'))
    training_id = request.POST.get('training_id')
    training = Training.objects.get(id=training_id)
    SetTrainingGoal(training,value)

    return JsonResponse({'status':'ok'})
# #end edit training plan

def SetRedisStartDatabase():
    r.set('training_count_0',0)
    r.set('training_count_1',0)
    r.set('training_count_2',0)


def DebugPrint(string,value):
    print(string + ': ' + str(value))


def DeletePlan(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        id = request.POST.get('id')
        context = {'status': 'ok'}
        boolRedirect = request.POST.get('redirect')
        plan = Training_plan.objects.get(id=id)
        plan.delete()

        return JsonResponse(context)
    else:
        return JsonResponse({'status': 'ko'})



# unit duration
def fGetUnitDuration(lDuration,sGoal):
    iMin = int(lDuration[0])
    iMax = int(lDuration[1])

    if iMin == iMax:
        
        return round(iMin,-1)
    else:
        iValue = random.randrange(iMin, iMax)
        return round(iValue,-1)
# #end unit duration


def GetSortedListOfTrainingGoalsWithoutPercentages(lGoals,iUnits):
    lUnit_goals = []
    if len(lGoals) == iUnits:  
        return lGoals    # end
    elif len(lGoals) < iUnits:  # more units than goals
        while True:
            for goal in lGoals:
                lUnit_goals.append(goal)
                if len(lUnit_goals) == iUnits:
                    break
    else:   # less units than goals
        lGoals = GetComprimisedTrainingGoalsList(lGoals)   # muscle, endurance, agility
        iGoals = len(lGoals)
        if iGoals > iUnits:
            if iUnits == 2:
                lUnit_goals.append(str(lGoals[1]) + str(lGoals[0]))
                lUnit_goals.append(str(lGoals[2])  + str(lGoals[0]))
            else:
                lUnit_goals.append(str(lGoals[2]) + str(lGoals[1]) + str(lGoals[0]))
    return lUnit_goals



def GetComprimisedTrainingGoalsList(lGoals):
    lResult = []
    sMuscle = ''
    sEndurance = ''
    for goal in lGoals:
        goal = str(goal)
        if goal == '0' or goal == '1' or goal == '2':  # muscle 
            sMuscle += goal         
        elif goal == '3' or goal == '4':  # endurance
            sEndurance += goal
        elif goal == '5':   # agility
            lResult.append(5)
    if sMuscle != '':
        lResult.append(sMuscle)
    if sEndurance != '':
        lResult.append(sEndurance)
    return lResult



def GetSortedListOfTrainingGoals(lGoals,iUnits,dGoal_percentage):
    listSortedTrainingGoalsOfAllDays = []
    if dGoal_percentage == '':
        listSortedTrainingGoalsOfAllDays = GetSortedListOfTrainingGoalsWithoutPercentages(lGoals,iUnits)
    else:
        listSortedTrainingGoalsOfAllDays = GetSortedListOfTrainingGoalsWithPercentages(lGoals,iUnits,dGoal_percentage)
    r.set('listSortedTrainingGoalsOfAllDays',json.dumps(listSortedTrainingGoalsOfAllDays))

    return listSortedTrainingGoalsOfAllDays


def GetSortedListOfTrainingGoalsWithPercentages(lGoals,intUnitsCount,dGoal_percentage):
    listGoalsOfAllDays = []
    lGoals_count = {}
    
    lSorted_goals = sorted(dGoal_percentage, key=dGoal_percentage.__getitem__,reverse=True)
    if len(lGoals) > intUnitsCount:
        print('more goals than untis')
        dNew_goal_percentage = GetComprimisedTrainingGoalsDictWithPercentage(dGoal_percentage,lSorted_goals)
        lSorted_goals = sorted(dNew_goal_percentage, key=dNew_goal_percentage.__getitem__,reverse=True)
        if  len(lSorted_goals) <= intUnitsCount:
            for i in range(intUnitsCount):
                listGoalsOfAllDays.append(-1)
            print('more goals than untis but comprimised it fits')
            for i in range(len(lGoals)):
                lGoals_count[lSorted_goals[i]] = round(0.01 * dNew_goal_percentage[lSorted_goals[i]] * intUnitsCount)  # count the days each goal were trained
                listGoalsOfAllDays = fGetUnitGoalsWithToManyGoals(intUnitsCount,lGoals_count[lSorted_goals[i]],i,listGoalsOfAllDays,lSorted_goals[i],iGoals)
        else:
            print('more goals than untis and comprimised also')
            listGoalsOfAllDays = fGetUnitGoalsWithToManyGoals(lSorted_goals,intUnitsCount)
    else:   # more units than goals
        listGoalsOfAllDays = GetSortedListOfTrainingGoalsWithMoreUnitsThanGoalsAndPercentage(intUnitsCount,dGoal_percentage,len(lGoals),lSorted_goals)


    return listGoalsOfAllDays


def GetSortedListOfTrainingGoalsWithMoreUnitsThanGoalsAndPercentage(intUnitsCount,dGoal_percentage,intMainGoalsCount,lSorted_goals):
    listGoalsOfAllDays = []
    lGoals_count = {}
    for i in range(intUnitsCount):
        listGoalsOfAllDays.append(-1)  # specify all days as not declared days
        # spread each goal on not declared days in range of all days 
        # dependant on percentage distribution
    for i in range(intMainGoalsCount):
        lGoals_count[lSorted_goals[i]] = round(0.01 * dGoal_percentage[lSorted_goals[i]] * intUnitsCount)         
        listGoalsOfAllDays = fGetUnit_goals_bool(intUnitsCount,lGoals_count[lSorted_goals[i]],i,listGoalsOfAllDays,lSorted_goals[i],intMainGoalsCount)
    return listGoalsOfAllDays


def fGetUnit_goals_bool(intUnitsCount,intDaysWithThisGoalCount,intMainGoalsIndex,listGoalsOfAllDays,goal,intMainGoalsCount):
    intRemainingMainGoalsCount = intDaysWithThisGoalCount
    iCount = 1
    for u in range(intUnitsCount):
        if u ==  intMainGoalsIndex and listGoalsOfAllDays[u] == -1:
            listGoalsOfAllDays[u] = goal
            intRemainingMainGoalsCount -= 1
        else:
            if listGoalsOfAllDays[u] == -1:
                if intRemainingMainGoalsCount > 0:
                    iFrequency = round((intUnitsCount-u) / intRemainingMainGoalsCount)
                    if iCount >= iFrequency:
                        listGoalsOfAllDays[u] = goal
                        iCount = 1
                        intRemainingMainGoalsCount -= 1
                    else:
                        if intMainGoalsIndex == (intMainGoalsCount -1): # if is last goal loop replace -1 with the goal
                            listGoalsOfAllDays[u] = goal
                            iCount = 1
                        else:
                            iCount += 1
                elif intMainGoalsIndex == (intMainGoalsCount -1): # if is last goal loop replace -1 with the goal
                    listGoalsOfAllDays[u] = goal

    return listGoalsOfAllDays
# #end plan generate



def fGetUnitGoalsWithToManyGoals(lSorted_goals,iUnits):
    lResult = []
    if iUnits == 2:
        lResult.append(lSorted_goals[0] + lSorted_goals[2])
        lResult.append(lSorted_goals[1] + lSorted_goals[2])
    else:
        lResult.append('')
        for goal in lSorted_goals:
            lResult[0] += goal
    return lResult


# get New goal percentages if to less units
def GetComprimisedTrainingGoalsDictWithPercentage(dGoal_percentage,lSorted_goals):
    sMuscle = sEndurance = ''
    iMuscle = iEndurance = 0
    dNew_goal_percentage = {}

    for goal in lSorted_goals:
        if goal == '0' or goal == '1' or goal == '2':
            sMuscle += goal
            iMuscle += dGoal_percentage[goal]
            
        elif goal == '3' or goal == '4':
            sEndurance += goal
            iEndurance += dGoal_percentage[goal]
        if goal == '5':
            dNew_goal_percentage.update({goal:dGoal_percentage[goal]})

    
    if sMuscle != '':
        dNew_goal_percentage.update({sMuscle:iMuscle})
    if sMuscle != '':
        dNew_goal_percentage.update({sEndurance:iEndurance})
    dNew_goal_percentage = sorted(dNew_goal_percentage)
    return dNew_goal_percentage
# #end get New goal percentages if to less units










# edit training plan
def fEditTrainingSets(request):
    sType = request.POST.get('type')

    if sType == 'add':
        iExercise_id = int(request.POST.get('exercise_id'))
        sKind = request.POST.get('kind')
        iPosition = int(request.POST.get('position'))
        iValue = int(request.POST.get('value'))
        exercise = IncludedExercise.objects.get(id=iExercise_id)
        new_set = Set.objects.none()
        if sKind == 'muscle_building':
            new_set = AddSetToExercise(exercise,iPosition,intRepeats=iValue - 2)
        elif sKind == 'endurance':
            new_set = AddSetToExercise(exercise,iPosition,timedeltaDuration=datetime.timedelta(minutes=iValue))
        else:
            new_set = AddSetToExercise(exercise,iPosition,timedeltaDuration=datetime.timedelta(seconds=iValue))


        sInput = fGetTrainingPlanDetailNumberField(sKind,iValue,iValue,iExercise_id,iPosition)
        sSet = '<div class="set">'+ fGetPlanSetChip(sKind,iPosition,iValue,sInput,'last',new_set.id,iExercise_id) + '</div>'
        context = {'set_html':sSet,'type':'add','id':iExercise_id}
        return JsonResponse(context)
    else:
        iId = int(request.POST.get('id'))
        oSet = Set.objects.get(id=iId)
        RemoveSetFromExercise(oSet)
        return JsonResponse({'type':'remove'})



def fEditAddTrainingDay(request):
    template = 'fitness/training_plans/detail/components/day_nav_item.html'
    sDay = request.GET.get('day')
    sPlan_id = request.GET.get('plan_id')
    training_plan = Training_plan.objects.get(id=int(sPlan_id))

    new_training = AddNewTrainingToPlan(training_plan,int(sDay) + 2)


    parts = {_('Ganzkörper'):0,_('Brust'):0,_('Bauch'):0}
    goals = Goal.objects.all()
    context = { 'ids':[id],
                'goals':goals,
                'parts': new_training.GetMainTrainedParts(),
                'main_parts': new_training.GetMainTrainedWorkoutParts(),
                'current_kind':'Muskelaufbau',
                'exercise_count':0,
                'is_first':False,
                'is_last': True,
                'training_id': new_training.id}
    return render(request,template,context)

def CreatePlanRequest(request):
    if request.is_ajax():
        if CheckIfValidUser(request):
            plan = CreateNewTrainingPlan(request.user)
            AddNewTrainingToPlan(plan)
            return TrainingPlanDetailView(request,plan.id,'neuer_plan')
        else:
            return JsonResponse({'status':'ko'})
    else:
        return fFitnessStartPage(request,page='training_plan_create')
    # #end post





# create
def fSaveOwner(request, plan, Member):
    if str(request.user) != 'AnonymousUser':

        owner = request.user
        print(str(owner))
        plan.owner = owner
    else:
        plan.owner = Member.objects.get(id=12)




def fGetExerciseBox (request):
    
    # varibles
    id = request.POST.get('id')
    main_kind = request.POST.get('main_kind')
    kind = request.POST.get('kind')
    
    unit_id = request.POST.get('unit_id')
    count_per_main_kind = request.POST.get('count')
    exercise = Exercise.objects.get(id=id)
    area = exercise.fGetAreaString()
    equipment = list(exercise.equipment.values_list('equipment',flat=True))
    exercise_serialized = ExerciseSerializer(exercise)
    exercise_serialized = exercise_serialized.data
    child_row  = ''
    img_style = 'width: 100%;height: 50px; border-radius: 50px; '\
    'box-shadow: inset 0 0 1px #e0e0e0, inset 0 0 14px rgba(0,0,0,0.2); ' \
    'position: relative;left: 50%;transform: translate(-50%,0); '
    img = '<img class="table_img" style="{}" src="{}"></img>'.format(img_style,exercise.image.url)
    weight_control_html = '<div class="btn-group" role="group" aria-label="Basic example">'\
  '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect minus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="weight"><i class="fas fa-minus"></i></button>'\
  '<input class="weight_input btn-outline-light-blue" min="0" name="exercise-exercises-'+ count_per_main_kind +'-sets-0-weight"'\
    'id="id_exercise-exercises-'+ count_per_main_kind +'-sets-0-weight" value="0" type="number" onfocus="fSetTotalDurationOnSetInputEdit(this)">'\
            '<div class="input-group-append"><span class="input-group-text btn-outline-light-blue">kg</span></div>'\
  '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect plus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="weight"><i class="fas fa-plus"></i></button>'\
  '</div>'
    repeats_control_html = '<div class="btn-group" role="group" aria-label="Basic example">'\
  '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect minus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="repeats"><i class="fas fa-minus"></i></button>'\
  '<input class="repeats_input btn-outline-light-blue" min="1" name="exercise-exercises-'+ count_per_main_kind +'-sets-0-reversrements"'\
   'id="id_exercise-exercises-'+ count_per_main_kind +'-sets-0-reversrements" value="12"  data-kind="repeats"  type="number" onfocus="fSetTotalDurationOnSetInputEdit(this)">'\
  '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect plus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="repeats"><i class="fas fa-plus"></i></button>'\
'</div>'
    duration_control_html = '<div class="btn-group" role="group" aria-label="Basic example">'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect minus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="endurance"><i class="fas fa-minus"></i></button>'\
    '<input class="endurance_input btn-outline-light-blue" min="1" value="10" type="number" data-kind="endurance"  onfocus="fSetTotalDurationOnSetInputEdit(this)">'\
    '<div class="input-group-append"><span class="input-group-text btn-outline-light-blue">Min.</span></div>'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect plus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="endurance"><i class="fas fa-plus"></i></button>'\
    '</div>'
    stretching_control_html = '<div class="btn-group" role="group" aria-label="Basic example">'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect minus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="stretching"><i class="fas fa-minus"></i></button>'\
    '<input class="stretching_input btn-outline-light-blue" min="1" value="40" type="number"  data-kind="stretching"  onfocus="fSetTotalDurationOnSetInputEdit(this)">'\
    '<div class="input-group-append"><span class="input-group-text btn-outline-light-blue">Sec.</span></div>'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect plus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="stretching"><i class="fas fa-plus"></i></button>'\
    '</div>'
    child_row_muscle = '<tr class="set"><td class="first-col"></td><td class="step"><span>1.</span></td>' \
    '<td class="weight sub_heading_col"><span class="sub_header">' + _('Gewicht') + ':</span><span>' + weight_control_html + '</span></td>' \
    '<td class="repeats sub_heading_col"><span class="sub_header">' + _('Wiederholungen') + ':</span><span>' + repeats_control_html + '</span></td></tr>'  
    child_row_stretching = '<tr  class="set">' \
    '<td class="first-col"></td><td class="step"><span>1.</span></td>' \
    '<td class="stretching sub_heading_col"><span class="sub_header">' + _('Dauer') + ':</span><span>' + stretching_control_html + '</span></td></tr>'  
    child_row_endurance = '<tr  class="set">' \
    '<td class="first-col"></td><td class="step"><span>1.</span></td>' \
    '<td class="duration sub_heading_col"><span class="sub_header">' + _('Dauer') + ':</span><span>' + duration_control_html + '</span></td></tr>'  
    set_control_html = '<div class="btn-group set-control" data-kind="' + kind + '" data-main_kind="' + main_kind + '" data-ex_id="' + str(exercise.id) + '" role="group" aria-label="Basic example" data-exercise_count="'+ count_per_main_kind +'">' \
    '<button type="button" class="btn btn-light-blue btn-rounded minus" data-kind="' + kind + '" data-unit_id="' + unit_id + '" data-main_kind="' + main_kind + '" onclick="fRemoveSetFromExercise(this)"><i class="fas fa-minus"></i></button>' \
    '<button type="button" class="btn btn-light-blue btn-rounded count">1</button>' \
    '<button type="button" class="btn btn-light-blue btn-rounded plus" data-kind="' + kind + '" data-unit_id="' + unit_id + '" data-exercise_count="'+ count_per_main_kind +'" data-main_kind="' + main_kind + '" onclick="fAddSetToExercise(this)"><i class="fas fa-plus"></i></button></div>' \
 
    delete = '<button type="button" class="btn btn-floating delete" onclick="fRemoveExerciseFromTable(this)" data-main_kind="' + main_kind + '" data-area="' + area + '" data-kind="' + kind + '"><i class="fas fa-trash-alt"></i></button>'

    # #end variables
        
            
                
        
    # set child_row_columns
    if exercise.fGetKindString() == 'muscle_building':
        child_table = child_row_muscle
    elif exercise.fGetKindString() == 'stretching':
        child_table = child_row_stretching
    else:
        child_table = child_row_endurance

    exercise_serialized.update({'main_kind':main_kind,'area':exercise.fGetAreaString(), 'child_table':child_table,'img':img,'sets':set_control_html,'equipment':equipment,'delete':delete})
    
    return JsonResponse(exercise_serialized)


def fGetExerciseSet(request):
    endurance_template = 'fitness/training_plans/member/manage/create/components/exercise_endurance_set.html'
    muscle_template = 'fitness/training_plans/member/manage/create/components/exercise_muscle_set.html'
    template = ''

    kind = request.GET.get('kind')
    main_kind =  request.GET.get('main_kind')
    step = request.GET.get('step')
    count = request.GET.get('count')
    exercise_count = request.GET.get('exercise_count')
    if kind == 'muscle_building':
        template = muscle_template
    else:
        template = endurance_template

    context = {'count':count,'step':step,'main_kind':main_kind,'exercise_count':exercise_count}
    return render(request,template,context)




# Detail Exercise view
def TrainingPlanDetailView(request,id,slug): 
    if request.is_ajax():
        plan = Training_plan.objects.get(id=id)
        recent_day = '1'
        if r.exists('recent_day'):
            recent_day = r.get('recent_day')
            r.delete('recent_day')
            recent_day = json.loads(recent_day.decode('utf-8'))
        template = 'fitness/training_plans/detail/detail.html'
        dTraining_days_ids = plan.fGetTrainingPlanDaysWithIds()
        days = list(dTraining_days_ids.keys())
        print(dTraining_days_ids)
        first_day_ids = list(dTraining_days_ids.values())[0]
        print('first day ids: ')
        print(first_day_ids)
        goals =  Goal.objects.all()
        context = {'plan':plan,'days':days,'first_day_ids':first_day_ids,'goals':goals,'recent_day':recent_day}
        return render(request,template,context)
    else:
        page = 'plan'
        context = {}
        return fFitnessStartPage(request,page,context)

def ChangeDayOfAllTrainings(request):
    iPlan_id = request.POST.get('plan_id')
    oPlan = Training_plan.objects.get(id=iPlan_id)

    lTrainings = oPlan.trainings.all()
    iDay_diff = lTrainings[0].day - 1     # start days from 1

    for training in lTrainings:
        iDay = training.day
        training.day = iDay - iDay_diff
        training.save()
    oPlan.save()
    return JsonResponse({'status':'ok'})


    

def Training_planGenerate(request):
    if request.is_ajax():
        template = 'fitness/training_plans/member/manage/generate/generate_base.html'

        goals = Goal.objects.order_by('identify')
        area_weaks = Goal.objects.filter(area_weak=True)
        context = {'goals':goals,'area_weaks':area_weaks}
        return render(request,template,context)
    else:
        page = 'training_plan_generate'
        print(page)
        return fFitnessStartPage(request,page)


def SaveData(request):

    r.set('recent_day',request.POST.get('day'))
    print('test day: ' + request.POST.get('day'))
    return JsonResponse({'status':'ok'})










# #end base
def fRoundUpEven(fNumber):
    iNumber = round(fNumber)
    if iNumber % 2 != 0:
        iNumber += 1
    return iNumber




# set
def fAddExerciseSetInEditMode(position,iDuration_seconds,included_exercise,sKind,iRepeats=None):
    new_set = Set.objects.create()
    new_set.position = position
    if sKind == 'muscle_building':
        new_set.reversrements = iRepeats
    else:
        
        if sKind == 'stretching':
            new_set.duration = datetime.timedelta(seconds=iDuration_seconds)
        else :
            new_set.duration = datetime.timedelta(seconds=iDuration_seconds)
    new_set.exercise = included_exercise
    new_set.save()
    return new_set.id
# #end set



def fGetExercisesTitles(request):
    lExercises_titles = list(Exercise.objects.all().values_list('title', flat=True))
    print(lExercises_titles)
    return JsonResponse(lExercises_titles,safe=False)


# get Plan input field
def fGetTrainingPlanDetailNumberField(sKind,iDuration,iRepeats,sIncl_ex_id,set):
    sUnit = ""
    iMin = 0
    iValue = iRepeats
    print(sKind)
    if sKind=='endurance':
        sUnit =  '<div class="input-group-append"><span class="input-group-text btn-outline-light-blue unit_text">Min.</span></div>'
        iMin = 1
        if type(iDuration) == datetime.timedelta:
            iValue = round(iDuration.seconds / 60)
        else:
            iValue = round(iDuration / 60)
    elif sKind=='stretching':
        sUnit =  '<div class="input-group-append"><span class="input-group-text btn-outline-light-blue unit_text">Sec.</span></div>'
        iMin = 1
        if type(iDuration) == datetime.timedelta:
            iValue = iDuration.seconds
        else:
            iValue = iDuration
        

    sInput = '<div class="btn-group" data-set="{}" role="group">'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect minus" onclick="fChangeInputByOneStepOnClick(this)" data-kind="{}" data-incl_ex_id="{}">-</button>'\
    '<input class="{}_input btn-outline-light-blue" min="{}" value="{}" type="number" data-kind="{}"  data-incl_ex_id="{}" onfocus="fSetTotalDurationOnSetInputEdit(this)">{}'\
    '<button type="button" class="btn btn-outline-light-blue btn-rounded waves-effect plus"  data-incl_ex_id="{}" onclick="fChangeInputByOneStepOnClick(this)" data-kind="{}">+</button>'\
    '</div>'.format(set,sKind,sIncl_ex_id,sKind,iMin,str(iValue),sKind,sIncl_ex_id,sUnit,sIncl_ex_id,sKind)
    print(sInput)
    return sInput
# #end get Plan input field


def GetExerciseSetsDom(e,kind,iTraining_id):
    iSet = e.sets.count()
    iHalf = math.ceil(iSet/2)
    lSets = e.sets.all()

    sets = '<div class="sets mx-auto" id="sets_{}"><div class="left">'.format(e.id)
    iSet_count = 1
    sSet_top = '<div class="set set_top">'
    for i in range(iSet):
        oSet = lSets[i]
        sLast = ''
        if (i == (iSet - 1)) and i != 0:
            sLast = 'last' 
        sInput = fGetTrainingPlanDetailNumberField(kind,oSet.duration,oSet.reversrements,e.id,i+1)
        if kind == 'muscle_building':
            sets += sSet_top + fGetPlanSetChip(kind,str(iSet_count),str(oSet.reversrements),sInput,sLast,oSet.id,iTraining_id) + '</div>'
        else:
            sets += sSet_top + fGetPlanSetChip(kind,iSet_count,oSet.duration.seconds,sInput,sLast,oSet.id,iTraining_id) + '</div>'
        if iHalf == iSet_count:
            sets += '</div><div class="right">'
            sSet_top = '<div class="set set_top">'
        if (iSet_count == 1) or (iSet_count == (iHalf+1)):
            sSet_top = '<div class="set">'
        iSet_count += 1
    sets += '</div></div><span class="add_btn text-center edit txt-c-d-1 h-100 bg-c-g-l-1 w-pct-80 mx-auto" data-kind="{}" data-exercise_id="{}" onclick="fAddSetToExercise(this)">Set hinzufügen</span>'.format(kind,e.id) # add btn

    return sets

def GetTrainingUnitDomExercise(e,iTraining_id,sShort_kind):
    area = e.exercise.fGetAreaString()
    equipment = list(e.exercise.equipment.values_list('equipment',flat=True))
    equipment = ', '.join(equipment)
    img = '<img class="table_img" src="{}"></img>'.format(e.exercise.image.url)
    kind = e.exercise.fGetKindString()
    sets = GetExerciseSetsDom(e,kind,iTraining_id)
    title = '<span class="title">{}</span>'.format(e.exercise.title)
    delete = '<i class="fas fa-trash bg-c-red-1" data-incl_ex_id="{}" data-kind="{}" data-training_id="{}" onclick="fDeleteExercise(this)"></i>'.format(e.id,sShort_kind,iTraining_id)
    print('inculuded exercise position: ')
    print(e.position)
    dNew_entry = {
        'img':img,
        'title':title,
        'area': area,
        'equipment':equipment,
        'sets':sets,
        'heading_class': sShort_kind + '_row rounded-sm', 
        'ex_id': e.id,
        'next_pos': str(int(e.position)),
        'kind': sShort_kind }
    return dNew_entry





def GetTrainingUnitData(iTraining_id,iUnit):
    training = Training.objects.get(id=iTraining_id)
    lTraining_entrys = []
    lMain_kinds = [training.warm_up,training.workout,training.cool_down]
    lsMain_kinds = [_('Aufwärmen'),_('Training'),_('Abwärmen')]
    lsShort_main_kinds = ['warm','train','cool']
    iKind_count = 0
    for main_kind in lMain_kinds:
        sShort_kind = lsShort_main_kinds[iKind_count]
        heading = sShort_kind   # for data row - class - to count exercises per kind
        title = '<span class="kind_heading">' + lsMain_kinds[iKind_count] + '</span>'
        dNew_entry =     {
            'img': '',
            'title': title,
            'equipment': '',
            'sets':'<span class="add_exercise txt-c-d-1 h-100 bg-c-g-l-1 text-center" data-kind="{}" data-training_id="{}" onclick="fAddExerciseToTrainingKind(this)">{}</span>'.format(sShort_kind,training.id,_('Übung hinzufügen')),
            'delete': '',
            'heading_class': heading + 'heading hp-30 bg-c-g-d-1 txt-c-l-1 p-0',
            'ex_id': '',
        }
        lTraining_entrys.append(dNew_entry)
        if str(main_kind) != 'None':
            for e in lMain_kinds[iKind_count].fGetExercises():
                lTraining_entrys.append(GetTrainingUnitDomExercise(e,iTraining_id,sShort_kind))

        iKind_count += 1
    return {'unit' : iUnit, 'training_id': iTraining_id, 'entries': lTraining_entrys}


def fGetTrainingData(request):
    template = 'fitness/training_plans/detail/components/table.html'
    training_plan_id = int(request.GET.get('plan_id'))
    lIds = request.GET.getlist('data')
    iUnit_count = 1
    lData = []

    for iTraining_id in lIds:
        lTraining_data = GetTrainingUnitData(iTraining_id,iUnit_count)
        lData.append(lTraining_data)
        iUnit_count += 1

    context= {'tables': lData,'training_plan_id':training_plan_id}
    return render(request,template,context)


def fGetPlanSetChip(sKind,sCount,iValue,sInput,sLast,iSet_id,iExercise_id):
    sSet = ''
    if sKind == 'muscle_building':
        sSet = '<div class="chip"><span class="count">{}.</span> <span class="text"><span class="value">{}'\
            '</span> mal</span><span class="input edit">{} <i class="close fas fa-times {}" data-id="{}" data-training_id="{}"'\
                ' onclick="fDeleteSet(this)"></i></span></div>'.format(sCount,iValue,sInput,sLast,iSet_id,iExercise_id)
    else:
        sDuration = ''
        iValue = iValue
        if sKind == 'endurance':
            sDuration = ' min.'
            iValue = round(iValue/60)   # count duration seconds to minutes for endurance exercises
        else:
            sDuration = ' sec.'
        sSet = '<div class="chip"><span class="count">{}.</span> <span class="text"><span class="value">{}</span>{}'\
            '</span><span class="input edit">{} <i class="close fas fa-times {}" data-id="{}" '\
                'data-training_id="{}" onclick="fDeleteSet(this)"></i></span></div>'.format(sCount,iValue,sDuration,sInput,sLast,iSet_id,iExercise_id)
    return sSet


def fGetSetDuration(sKind,sMain_kind):
    if sKind == 'stretching':
        return 40  # 40s for stretching exercise
    elif sMain_kind == 'warm':
        return 900 # 900s = 15min for endurance exercise in warm up
    elif sMain_kind == 'train':
        return 1200   # 20min for training 
    else:
        return 480  # 8min for cool down




def fAddExerciseToPlan(request):
    template = 'fitness/training_plans/detail/components/exercise.html'
    iId = request.GET.get('id')
    sMain_kind = request.GET.get('main_kind')
    sKind = request.GET.get('kind')
    iTraining_id = request.GET.get('training_id')
    sPos = request.GET.get('pos')

    exercise = Exercise.objects.get(id=iId)

    oTraining = Training.objects.get(id=iTraining_id)
    iDuration = fGetSetDuration(sKind,sMain_kind)    # get set duration for stretchin and endurance exercise

    included_exercise = AddNewExerciseToTraining(exercise,sPos,oTraining,sMain_kind)

    
    set_id = fAddExerciseSetInEditMode(1,iDuration,included_exercise,sMain_kind,12)


    context = GetTrainingUnitDomExercise(included_exercise,iTraining_id,sMain_kind)

    return render(request,template,context)


def RemoveExerciseFromTraining(stringKind,objectTraining,objectInclExercise):
    if stringKind == 'warm':
        objectTraining.warm_up.exercises.remove(objectInclExercise)
    elif stringKind == 'train':
        objectTraining.workout.exercises.remove(objectInclExercise)
    else:
        objectTraining.cool_down.exercises.remove(objectInclExercise)


def fRemoveExerciseFromPlan(request):
    iId = request.POST.get('id')
    iTraining_id = request.POST.get('training_id')
    training = Training.objects.get(id=iTraining_id)
    incl_ex = IncludedExercise.objects.get(id=iId)
    sMain_kind = request.POST.get('kind')
    RemoveExerciseFromTraining(sMain_kind,training,incl_ex)
    training.save()
    incl_ex.delete()
    return JsonResponse({'status':'ok'})


def CheckIfMainAreasOrderIsChanged(request):
    stringKind = request.POST.get('kind')
    number = int(request.POST.get('number'))
    exercise = IncludedExercise.objects.get(id=request.POST.get('incl_ex_id'))
    training = Training.objects.get(id=request.POST.get('training_id'))
    areasChanges = None
    if '0' or '1' or '2' in training.goal.identify:
        areasChanges = AddOrRemoveExerciseTrainingMusclesList(exercise,training,number,stringKind)
    else:
        areasChanges = AddOrRemoveExerciseTrainingAreasList(exercise,training,number,stringKind)
    training.save()
    return JsonResponse({'areasChanges': areasChanges})


def AddOrRemoveExerciseTrainingAreasList(exercise,training,intNumber=1,stringKind=''):
    areasChanges = []
    areasChanges.append(training.AddOrRemoveExerciseAreasList(exercise,intNumber))

    if stringKind == 'train':                            # check if exercise is added to workout
        areasChanges.append(training.AddOrRemoveExerciseWorkoutAreasList(exercise,intNumber))
    else:
        areasChanges.append(None)

    return areasChanges

def AddOrRemoveExerciseTrainingMusclesList(exercise,training,intNumber=1,stringKind=''):
    areasChanges = []
    areasChanges.append(training.AddOrRemoveExerciseMusclesList(exercise,intNumber))

    if stringKind == 'train':                            # check if exercise is added to workout
        areasChanges.append(training.AddOrRemoveExerciseWorkoutMusclesList(exercise,intNumber))
    else:
        areasChanges.append(None)

    return areasChanges



def fEditInputChanges(request):
    dData = request.POST.get('data')

    print(dData)
    dData = json.loads(dData)
    print(dData)
    if dData:
        for key, value in dData.items():
            exercise = IncludedExercise.objects.get(id=key)
            sKind = value[0]
            for set, set_value in value[1].items():
                eSet = exercise.sets.filter(position=set)[0]
                print(eSet.id)
                if sKind == 'muscle_building':
                    eSet.reversrements = int(set_value)
                elif sKind == 'endurance':
                    eSet.duration = datetime.timedelta(minutes=int(set_value))
                else:
                    eSet.duration = datetime.timedelta(seconds=int(set_value))
                eSet.save()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ko'})


def fEditOrderChanges(request):
    lExercises_per_kind = []    # warm, train, cool
    lExercises_per_kind.append(json.loads(request.POST.get('warm_exercises')))
    lExercises_per_kind.append(json.loads(request.POST.get('train_exercises')))
    lExercises_per_kind.append(json.loads(request.POST.get('cool_exercises')))
    print(lExercises_per_kind)
    for dExercises_per_kind in lExercises_per_kind:
        print(dExercises_per_kind)
        for key, value in dExercises_per_kind.items():
            exercise = IncludedExercise.objects.get(id=key)
            exercise.position = value
            exercise.save()

    return JsonResponse({'status':'ok'})


def fEditUnitsOrderChanges(request):
    dUnit_ids_per_days = json.loads(request.POST.get('dData'))
    print(dUnit_ids_per_days)
    for key, value in dUnit_ids_per_days.items():
        for training_id in value:
            training = Training.objects.get(id=training_id)
            training.day = key
            training.save()
    return JsonResponse({'status':'ok'})



def fEditDeleteDay(request):
    lIds = request.POST.getlist('data')
    for id in lIds:
        training = Training.objects.get(id=id)
        print('delete training: ')
        print(training)
        training.delete()

    return JsonResponse({'status':'ok'})


# plan create components
def fCreateWarmUpWorkoutCoolDown():
    warm_up = WarmUp.objects.create()
    warm_up.save()
    workout = Workout.objects.create()
    workout.save()
    cool_down = CoolDown.objects.create()
    cool_down.save()

    return [warm_up,workout,cool_down]





def fEditAddDayLabel(request):
    template = 'fitness/training_plans/detail/components/day_label.html'
    day = request.GET.get('day')
    context = {'day':day,'is_first':False}
    return render(request,template,context)
# #end edit training plan
















#def CreateTrainingFirstVersion(request):
#    template_begin = 'fitness/training_plans/member/manage/create/create_base.html'
#    template_training_unit = 'fitness/training_plans/member/manage/create/components/training_unit.html'
#    template_exercises_search_dialog_content = 'fitness/training_plans/exercises_search/content.html'
#    excluded_euq_queryset = Equipment.objects.none()
#    kinds = Kind.objects.none()
#    exercises_context = {}
#    exercises_context_list = []
#    unit_number = request.POST.get('unit_number')
#    print('create tr pl post fct begin')
#
#    if unit_number == 'begin':
#        formset = forms.Training_planStartPageForm()
#        indoor_equ = Equipment.objects.filter(kind='indoor')
#        outdoor_equ = Equipment.objects.filter(kind='outdoor')
#        light_equ = Equipment.objects.filter(kind='light')
#        context = {'form':formset,'light_equ':light_equ,'outdoor_equ':outdoor_equ,'indoor_equ':indoor_equ}
#        return render(request,template_begin,context)
#    # #end begin form
#    else:
#        # first unit form
#        context = {}
#        if unit_number == '1':
#            print('create training plan next step = 1')
#            formset = forms.Training_planStartPageForm(data = request.POST)
#            if formset.is_valid():
#                excluded_euq_queryset = formset.cleaned_data['excluded_equipment']
#                kinds = formset.cleaned_data['exercise_kinds']
#                print(excluded_euq_queryset)
#                fGetAndSetExercisesContextCorrespondingToUserWishes(kinds,excluded_euq_queryset,True)
#        kinds = r.get('exercises_kinds')
#        kinds = json.loads(kinds.decode('utf-8'))
#        print(kinds)
#        print(unit_number)
#        next_unit_number= str(int(unit_number)+1)
#        unit_id = request.POST.get('unit_id')
#        prev_unit_number= str(int(unit_number)-1)
#        context.update( { 
#                     'kinds':kinds,'prev_unit_number':prev_unit_number,'next_unit_number':next_unit_number,'unit_id':unit_id,'unit_number':unit_number})
#        print('create training plan get next page before return render')
#        return render(request,template_training_unit,context)
def fGetNewNumberCircle(request):
    page = 'fitness/training_plans/member/manage/create/components/new_number_circle.html'
    context = {'number':request.GET.get('number'),'id':request.GET.get('unit_id')}
    return render(request,page,context)
# #end training plan create 


def fTrainingPlanCreateSave(request):
    list_template =  'fitness/training_plans/member/list/list.html'
    sData = request.POST.get('data')
    dData = json.loads(sData)
    print(dData)
    new_training_plan = Training_plan.objects.create()
    iTraining_day = 1
    count = 1

    for unit, unit_data in dData.items():
        print(unit)
        if unit == 'title':
            print(unit)
            new_training_plan.title = unit_data
        elif unit == 'main_kind':
            print(unit_data)
            new_training_plan.kinds_count = unit_data
        else:
            new_training = Training.objects.create()

            for sMain_kind, lExercises in unit_data.items():
                print(sMain_kind)
                if sMain_kind == 'duration':
                    new_training.duration = datetime.timedelta(minutes=int(lExercises[0]))
                elif sMain_kind == 'title':
                    new_training.title = lExercises
                elif sMain_kind == 'day':
                    new_training.day = lExercises
                else:
                    if len(lExercises) > 0:
                        new_main_kind = None
                        if sMain_kind == 'warm':
                            new_main_kind = WarmUp.objects.create()
                            new_training.warm_up = new_main_kind
                        elif sMain_kind == 'train':
                            new_main_kind = Workout.objects.create()
                            new_training.workout = new_main_kind
                        else:
                            new_main_kind = CoolDown.objects.create()
                            new_training.cool_down = new_main_kind
                        for lExercise_data in lExercises:
                            included_exercise = IncludedExercise.objects.create()
                            exercise = Exercise.objects.get(id=lExercise_data[0])
                            print(exercise)
                            included_exercise.exercise = exercise
                            needed_equipment = exercise.equipment.all()
                            if needed_equipment:
                                print(needed_equipment)
                                for e in needed_equipment:
                                    new_training_plan.needed_equipment.add(e)
                            for lSet in lExercise_data[1]:
                                print(lSet)
                                new_set = Set.objects.create()

                                new_set.position = int(lSet[0])
                                lSet_info = lSet[1]
                                if len(lSet_info) > 1:
                                    new_set.weight = lSet_info[0]
                                    new_set.reversrements = lSet_info[1]
                                else:
                                    if exercise.fGetKindString() == 'endurance':
                                        new_set.duration = datetime.timedelta(minutes=int(lSet_info[0]))
                                    else:
                                        new_set.duration = datetime.timedelta(seconds=int(lSet_info[0]))
                                new_set.exercise = included_exercise
                                new_set.save()
                            if sMain_kind == 'warm':
                                included_exercise.warm_up = new_main_kind
                            elif sMain_kind == 'train':
                                included_exercise.workout = new_main_kind
                            else:
                                included_exercise.cool_down = new_main_kind
                            included_exercise.save()
                        new_main_kind.save()
            new_training.save()
        
        #data[count] = [new_training.__str__() ,  str(int((new_training.duration.seconds/60))) , str(new_training.id)]
        count += 1
        new_training_plan.trainings.add(new_training)

    new_training_plan.save()
    #context = {'data':json.dumps(data)}
    plans = Training_plan.objects.all()
    context = {'plans':plans}
    return render(request,list_template,context)
