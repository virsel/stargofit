from django import template
from training_plans.models import Exercise, eMuscleBuilding, eEnduranceTraining
import os
from stargofit.settings.base import BASE_DIR
from pathlib import Path
from training_plans.views.exercises import fGetPaginatedResponse
from django.db.models import Q
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def setvar(var):
    return var


@register.simple_tag
def pluralize(string, count):
    if count > 1:
        string = string + 'n'
    return string


@register.simple_tag
def SetCompositVar(var_1, var_2):
    return var_1 + str(var_2) + '.svg'


@register.simple_tag
def Set_image_url_var(var_1, var_2):
    return var_1 + str(var_2) + '.png'


@register.simple_tag(takes_context=True)
def bNext_is_other_muscle_kind(context, iExercise_index, eCurrent_exercise_muscle, sExerciseKind):
    if iExercise_index < (context['exercises'].count()-1):
        eNext_exercise = context['exercises'][(iExercise_index+1)]
        if sExerciseKind == 'muscle_building':
            return eNext_exercise.muscle != eCurrent_exercise_muscle
        else:
            return eNext_exercise.endurance_training.area != eCurrent_exercise_muscle
    return True


@register.simple_tag
def tMedia(sUrl):
    sUrl = Path('static_files' + sUrl)
    sUrl = os.path.join('file:/', BASE_DIR, sUrl).replace("\\", "/")
    return sUrl


@register.simple_tag(takes_context=True)
def tfGetExercisePercentage(context):
    percentage = context['exercise'].iGetPercentage()
    return percentage


@register.simple_tag
def plural(sString, value):

    if value > 1 or value == 0:
        bGerman = ('de' == get_language())
        sNew_string = ''
        chLast_char = sString[-1:]
        print(chLast_char)
        if bGerman:
            if chLast_char in 'e':
                sNew_string = sString + 'n'
            elif chLast_char in 'tgr':
                sNew_string = sString + 'e'
        else:
            sNew_string = sString + 's'
        return sNew_string
    else:
        return sString
