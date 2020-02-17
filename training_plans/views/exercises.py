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
from ..models import Equipment, Training_plan, Kind, Area,Training, WarmUp,Workout,CoolDown, IncludedExercise, Set, CustomRating, CurrentPlan,Exercise, eEnduranceTraining, eMuscleBuilding,eStretching
from .. import forms
from ..serializers import ExerciseSerializer

from .views import fFitnessStartPage


r = redis.Redis()

# all exercises view
#@cache_page(60 * 15)
def ExercisesListView(request,slug=None): 
    if request.is_ajax():
        range = ['x','x','x','x','x']
        kind = request.POST.get('kind')
        exercises = Exercise.objects.filter(kind__identify=kind)
        exercises_ids = list(exercises.values_list('id', flat=True))
        r.set('exercises_list_ids',json.dumps(exercises_ids))
        exercises = fGetPaginatedResponse('true',exercises,1)
        template_name = 'fitness/exercises/list/all_exercises_start_list.html'
        context = {'exercises': exercises,'range':range}
        return render(request,template_name,context)
    else:
        return fFitnessStartPage(request,page='all_exercises')
# ###end### all exercises view

def fGetExercisesPerKind(kind):
    exercises = Exercise.objects.none()
    if kind == 'endurance':
        exercises = eEnduranceTraining.objects.all()
    elif kind == 'muscle_building':
        exercises = eMuscleBuilding.objects.all()
    else:
        exercises = eStretching.objects.all()
    return exercises


def fGetExercisesAfterSearch(sSearch,exercises):
    exercises = exercises.filter(title__icontains=sSearch)
    return exercises

# get exercises for specific conditions
def fGetExercisesPerConditionsFunction(page,sField,lsNames,liEfficiency,liDifficulty,iEquipment,exercises,sOn_scroll):

    # muscle shape selection
    if sField == 'muscle': 
        cache_exercises = Exercise.objects.none()
        for name in lsNames:  
            cache_exercises = cache_exercises | exercises.filter(muscle=name) 
        exercises = cache_exercises
    elif sField == 'area':
        cache_exercises = Exercise.objects.none()
        for name in lsNames:  
            cache_exercises = cache_exercises | exercises.filter(area__identify=name) 
        exercises = cache_exercises
    # ###end### muscle shape selection


    if not iEquipment == '3':
    
        if iEquipment == '1':
            exercises = exercises.filter(~Q(equipment=None))
        else:
            print(str(exercises)) 
            exercises = exercises.filter(equipment=None)
        

    if not (liEfficiency[0] == '1' and liEfficiency[1] == '5'):
        iMin_value = int(liEfficiency[0])
        iMax_value = int(liEfficiency[1])              
        exercises = exercises.filter(efficiency__range=(iMin_value,iMax_value))
    if not (liDifficulty[0] == '1' and liDifficulty[1] == '5'):
        iMin_value = int(liDifficulty[0])
        iMax_value = int(liDifficulty[1])              
        exercises = exercises.filter(difficulty__range=(iMin_value,iMax_value))
    # ###end### filtering
    return exercises
# ###end### get exercises for specific conditions



def fGetExercisesTitles(request):
    lExercises_titles = list(Exercise.objects.all().values_list('title', flat=True))
    print(lExercises_titles)
    return JsonResponse(lExercises_titles,safe=False)


def SearchForExercises(request):
    range = ['x','x','x','x','x']
    if request.method == 'POST':
        try:
            kind = request.POST.get('kind')
            sSearchTerm = request.POST.get('search')
            exercises = fGetExercisesPerKind.filter(title__icontains=sSearchTerm)
            exercises = fGetPaginatedResponse('false',exercises,request.POST.get('page'))
            return render(request,'fitness/exercises/list/ajax_exercises_first_page.html',{'sub_sub_section':kind,'sub_section':'all_exercises','section':'fitness','exercises':exercises,'range':range})
                
        except KeyError:
            return HttpResponse(status=204)



def fGetExercisesPerConditions(request):
    range = ['x','x','x','x','x']

    if request.method == 'POST':
        exercises = Exercise.objects.none()
        page = request.POST.get('page')
        sOn_scroll = request.POST.get('sOn_scroll')
        template = 'fitness/exercises/list/ajax_exercises.html'
        if sOn_scroll == 'false':    
            sSearch = request.POST.get('search')
            template = 'fitness/exercises/list/ajax_exercises_first_page.html'
            if sSearch != '':
                exercises = Exercise.objects.all()
                exercises = fGetExercisesAfterSearch(sSearch,exercises)   
            else:
                sKind = request.POST.get('kind')
                sField = request.POST.get('field')
                lsNames = request.POST.getlist('names')
                lsEfficiency = request.POST.getlist('lEfficiency')
                lsDifficulty = request.POST.getlist('lDifficulty')
                iEquipment = request.POST.get('iEquipment')
                exercises = fGetExercisesPerKind(sKind)
                exercises = fGetExercisesPerConditionsFunction(page,sField,lsNames,lsEfficiency,lsDifficulty,iEquipment,exercises,sOn_scroll)     
            exercises_ids = list(exercises.values_list('id', flat=True))
            r.set('exercises_list_ids',json.dumps(exercises_ids))
        else:
            exercises_ids = r.get('exercises_list_ids')
            exercises_ids = json.loads(exercises_ids.decode('utf-8'))
            exercises = Exercise.objects.filter(id__in=exercises_ids)
        exercises = fGetPaginatedResponse(sOn_scroll,exercises,page)
        return render(request,template,{'exercises':exercises,'range':range})



# get Exercise result per page function
def fGetPaginatedResponse(sOn_scroll,objects,page):
    paginator = Paginator(objects,6)
    try:
        exercises = paginator.page(page)
        return exercises
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        exercises = paginator.page(1)
        return exercises
    except EmptyPage:
        if sOn_scroll == 'true':
            # if the reuqest is AJAX and the page is out of range return an empty page
            return None
        #if page is out of range deliver last page of results
        return paginator.page(paginator.num_pages)
    # section variable to track the site's section that the user is browsing

def ExerciseSelectionSmallWindowFirst(request):
    template = 'fitness/training_plans/detail/components/exercise_selection_small_window/step_1.html'
    kinds =     (('0', _('Muskel und Kraftaufbau')),
                ('1', _('Ausdauer')),
                ('2', _('Beweglichkeit')),)
    context = {'kinds': Kind.objects.all()}
    return render(request,template,context)


def ExerciseSelectionSmallWindowSecond(request):
    template = 'fitness/training_plans/detail/components/exercise_selection_small_window/step_2.html'
    sKind = request.GET.get('kind')
    context = {}
    areas = Area.objects.all()
    if sKind == 'endurance':
        exercises = fGetExercisesPerKind('endurance')
        context = {'exercises':exercises,'boolBack_to_step_two': False}
        template = 'fitness/training_plans/detail/components/exercise_selection_small_window/step_3.html'
    else:
        context = {'areas':areas,'kind':sKind}

    return render(request,template,context)


def ExerciseSelectionSmallWindowThird(request):
    template = 'fitness/training_plans/detail/components/exercise_selection_small_window/step_3.html'
    sArea = request.GET.get('area')
    sKind = request.GET.get('kind')
    exercises = fGetExercisesPerKind(sKind)
    exercises = exercises.filter(area__identify=sArea)
    context = {'exercises':exercises,'boolBack_to_step_two': True,'kind':sKind}

    return render(request,template,context)


def fGetExercisesDialog(request):
    bGet_exercises_for_dialog = request.POST.get('bExercises')
    bGet_exercise_titles_for_autocomplete = request.POST.get('bAutocomplete')
    template = 'fitness/training_plans/exercises_search/content.html'
    bIs_edit_dialog = request.POST.get('bIs_edit_dialog')
    if bIs_edit_dialog == "true":
        if bGet_exercise_titles_for_autocomplete == "true":
            exercises_ids = list(exercises.values_list('id', flat=True))
            exercises_titles = list(exercises.values_list('title', flat=True))
            return JsonResponse({'exercises_ids':exercises_ids,'exercises_titles':exercises_titles})
        else:
            
            context = {}
            kinds = Kind.objects.all().values_list('identify','kind')
            exercises = Exercise.objects.all()
            areas = Area.objects.all()
            context = {'exercises':exercises,'count':exercises.count(),'areas':areas,'kinds':kinds}
    else:
        if bGet_exercise_titles_for_autocomplete == "true":
            exercises_ids = r.get('exercises_ids')
            exercises_ids = json.loads(exercises_ids.decode('utf-8'))
            exercises_titles = r.get('exercises_titles')
            exercises_titles = json.loads(exercises_titles.decode('utf-8'))
            return JsonResponse({'exercises_ids':exercises_ids,'exercises_titles':exercises_titles})
        else:
            context = fGetAndSetExercisesContextCorrespondingToUserWishes(None,None,False)
    return render(request,template,context)


def fGetAndSetExercisesContextCorrespondingToUserWishes(qKinds, equ_exclusion,bSet):

    # set exercise query in redis database
    if bSet:
        exercises = Exercise.objects.all()
        bKinds = qKinds.count() > 0
        bExl = equ_exclusion.count() > 0
        if bKinds and bExl:
            exercises = exercises.filter(kind__in=qKinds).exclude(equipment__in=equ_exclusion)
        elif bKinds:
            exercises = exercises.filter(kind__in=qKinds)
        elif bExl:
            exercises = exercises.exclude(equipment__in=equ_exclusion)
        
        if not bKinds:
            qKinds = Kind.objects.all()
        kinds = list(qKinds.values_list('identify','kind'))

        r.set('exercises_kinds',json.dumps(kinds))

        exercises_ids = list(exercises.values_list('id', flat=True))
        exercises_titles = list(exercises.values_list('title', flat=True))

        r.set('exercises_ids',json.dumps(exercises_ids))
        r.set('exercises_titles',json.dumps(exercises_titles))
    # #end set exercise query in redis database


    # get saved exercises query form redis database
    else:
        exercises_ids = r.get('exercises_ids')
        exercises_ids = json.loads(exercises_ids.decode('utf-8'))
    
        print(len(list(exercises_ids)))
        exercises = Exercise.objects.filter(id__in=exercises_ids)

        areas = (
            ('arms', 'Arme'),
            ('chest', 'Brust'),
            ('legs', 'Beine'),
            ('back', 'Rücken'),
            ('glutes', 'Po'),
            ('bauch', 'Bauch'),
            ('shoulder', 'Schultern'),
            ('full', 'Ganzkörper'),
        )
        count = str(exercises.count())
        kinds = r.get('exercises_kinds')
        kinds = json.loads(kinds.decode('utf-8'))

        context = {'exercises':exercises,'count':count,'areas':areas,'kinds':kinds}
        return context
        # #end get saved exercises query form redis database
