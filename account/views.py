from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import *
from .models import Profile, Member
from django.contrib import messages
from common.decorators import ajax_required
from .models import Contact
import json
from django.core import serializers
from django.views.generic.base import TemplateResponseMixin, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.core.cache import cache
from .authentication import authenticate
from training_plans.models import Training_plan, CurrentPlan


def ProfileView(request):
    if request.is_ajax():
        print('profile is ajax')
        template = 'account/dashboard/components/profile.html'
        context = {'current_plan': '',
                   'recent_training': '', 'member': request.user}
        current_plan = CurrentPlan.objects.none()
        try:
            current_plan = request.user.current_plan
        except Exception as e:
            print(e)
        if current_plan != CurrentPlan.objects.none():
            recent_training = current_plan.GetRecentTraining()
            print(recent_training)
            context.update({'recent_training': recent_training,
                            'current_plan': current_plan})

        return render(request, template, context)

    if request.method == 'POST':
        print('profile post method')
        member = request.user

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate member, returns Member if successfully
            member = authenticate(
                request, email=cd['email'], password=cd['password'])
            if member is not None:
                login(request, member,
                      backend='django.contrib.auth.backends.ModelBackend')
                return DashboardStartView(request, 'profile')
            else:
                return JsonResponse({'status': 'false'})
        else:
            print(form.errors)
            return JsonResponse({'status': 'invalid'})

    return DashboardStartView(request, 'profile')


@csrf_protect
def member_login(request):

    template = 'administration/login.html'
    context = {}
    return render(request, template, context)


@csrf_protect
def member_logout(request):
    logout(request)
    return redirect("start_page")


@csrf_protect
def register(request):
    if request.method == 'POST':
        print(request.POST)
        member_form = MemberRegistrationForm(request.POST)
        print('register 1')
        if member_form.is_valid():
            template_name = 'account/dashboard.html'
            # Create a new member object but avoid saving it yet
            new_member = member_form.save(commit=False)
            # Set chosen password, handles encryption for savety
            new_member.set_password(member_form.cleaned_data['password'])
            new_member.save()
            # creates an empty profile associated with them
            Profile.objects.create(member=new_member)
            return render(request, template_name, {'new_member': new_member})
        else:
            print(member_form.errors)
    else:
        template = 'administration/register.html'
        context = {}
        return render(request, template, context)


@login_required
def ProfileSettingsView(request):
    if request.is_ajax():
        template = 'account/dashboard/components/edit.html'
        context = {}
        return render(request, template, context)
    if request.method == 'POST':
        # for storing data in the built in member model
        member_form = MemberEditForm(
            instance=request.user, data=request.POST)
        # for storing additional profile data in the custom profile model
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if member_form.is_valid() and profile_form.is_valid():
            member_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    return DashboardStartView(request, 'settings')


def DashboardStartView(request, page='profile'):
    template_name = 'account/dashboard/dashboard.html'
    context = {'page': page}

    print(template_name)
    return render(request, template_name, context)


def ProfilePlansView(request):
    if request.is_ajax():
        template = 'fitness/training_plans/list/list.html'
        plans = request.user.training_plans_created.all()
        context = {'plans': plans}
        return render(request, template, context)
    else:
        return DashboardStartView(request, 'member_plans')


def ProfileFavoritesView(request):
    if request.is_ajax():
        template = 'fitness/training_plans/list/list.html'
        plans = request.user.favorite_plans.all()
        context = {'plans': plans}
        return render(request, template, context)
    else:
        return DashboardStartView(request, 'member_favorites')
