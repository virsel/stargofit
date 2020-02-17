from django.shortcuts import render
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.response import Response
import json
import math
import random
import redis
import datetime


from account.models import LikeDislike, Member
from ..models import Equipment, Training_plan, Kind, Area, Training, WarmUp, Workout, CoolDown, IncludedExercise, Set, CustomRating, CurrentPlan, Exercise, eEnduranceTraining, eMuscleBuilding, eStretching
from .. import forms
from ..serializers import ExerciseSerializer


r = redis.Redis()


# ###end### training plans member mixins
def fFitnessStartPage(request, page='start', context={}):
    template_name = 'fitness/base_fitness.html'
    context = {'page': page}
    context.update(context)
    if request.is_ajax():
        template_name = 'fitness/start_page.html'
    else:
        areas = Area.objects.all()
        context.update({'areas': areas})

    return render(request, template_name, context)


# member training plan list, create, edit and delete view
def MemberTraining_planList(request):
    template_name = 'fitness/training_plans/member/list/list.html'
    qs = Training_plan.objects.all()
    context = {'plans': qs}
    return render(request, template_name, context)


# member training plan list, create, edit and delete view
def AllTraining_planList(request):
    print('MemberTraining_planListView begin')
    if request.is_ajax():
        qs = Training_plan.objects.all()
        template_name = 'fitness/training_plans/list/list.html'
        context = {'plans': qs, }
        return render(request, template_name, context)
    else:
        return fFitnessStartPage(request, 'all_training_plans')


def fGetExerciseVideo(request):
    id = request.GET.get('id')
    exercise = Exercise.objects.get(id=int(id))
    context = {'exercise': exercise}
    template = 'fitness/exercises/list/card/components/video.html'
    return render(request, template, context)


# Detail Exercise view
def ExerciseDetailView(request, id, slug):
    if request.is_ajax():
        exercise = Exercise.objects.get(id=id)
        user = request.user
        rating = 0
        if str(user) != 'AnonymousUser':
            print(str(user))
            oUser_rating = exercise.rating.filter(member=user)
            print(str(oUser_rating))
            if oUser_rating:
                rating = oUser_rating[0].rating
        template = 'fitness/exercises/detail/detail.html'
        range = ['x', 'x', 'x', 'x', 'x']  # for star rating
        context = {'exercise': exercise, 'range': range, 'user_rating': rating}
        print(rating)
        return render(request, template, context)
    else:
        page = 'exercise'
        print(page)
        return fFitnessStartPage(request, page)


class VotesView(View):
    model = None  # images
    vote_type = None  # like or dislike

    def post(self, request):
        id = request.POST.get('pk')
        status = 'ko'

        obj = get_object_or_404(self.model, id=id)
        # GenericForeignKey does not support get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(
                obj), object_id=obj.id, member=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=('vote',))

                #

                result = True
            else:
                likedislike.delete()
                result = False

        except LikeDislike.DoesNotExist:
            obj.votes.create(member=request.user, vote=self.vote_type)
            result = True

        status = 'ok'
        percentage = obj.iGetPercentage()
        obj.like_percentage = percentage
        obj.save()
        return HttpResponse(json.dumps({'status': status, 'percentage': percentage}), content_type="application/json")


def ExerciseRating(request):
    id = request.POST.get('id')
    rating = request.POST.get('rating')
    user = request.user
    print(user)
    if str(user) != 'AnonymousUser':

        cOld_rating = CustomRating.objects.filter(member=user, object_id=id)
        exercise = Exercise.objects.get(id=id)
        print(cOld_rating)
        if len(cOld_rating) > 0:
            cOld_rating = cOld_rating[0]
            print('rating refreshed')
            cOld_rating.rating = rating
            cOld_rating.save()
            rating = exercise.rating.fGetRatingResult()
            print(rating)
            return JsonResponse({'user': 'ok', 'rating': rating})
        else:
            cRating = CustomRating.objects.create(rating=rating, member=user)
            cRating.save()
            exercise.rating.add(cRating)
            rating = exercise.rating.fGetRatingResult()
            print(rating)
            return JsonResponse({'user': 'ok', 'rating': rating})
    else:
        return JsonResponse({'user': 'no'})


def ChangeFavoritesListOfPlan(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        id = request.POST.get('id')
        bFavorite = request.POST.get('favorite') == 'true'
        context = {'status': 'ok'}
        plan = Training_plan.objects.get(id=id)
        member = Member.objects.get(id=request.user.id)

        if bFavorite:
            plan.favorite_from.remove(member)
            context.update({'member': 'yes member removed'})
        else:
            plan.favorite_from.add(member)
        plan.save()
        return JsonResponse(context)
    else:
        return JsonResponse({'status': 'ko'})


def ChangeCurrentPlanStatus(request):
    user = request.user
    if str(user) != 'AnonymousUser':
        bCurrent_plan = request.POST.get('current_plan') == 'true'
        if bCurrent_plan:   # if user has already a current plan...
            user.current_plan.RemovePlan()
            user.current_plan.save()
            return JsonResponse({'status': 'ok, plan has been removed'})
        else:
            id = request.POST.get('id')
            current_plan = CurrentPlan.objects.none()
            try:
                current_plan = user.current_plan
            except:
                current_plan = CurrentPlan.objects.create()
                current_plan.member = user
            current_plan.SetNewPlan(id)
            current_plan.save()
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ko'})
