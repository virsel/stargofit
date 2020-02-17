from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory, BaseModelForm, BaseInlineFormSet
from .models import Training_plan, Equipment,  Kind, Training, Set, Exercise, IncludedExercise, WarmUp, CoolDown, Workout
from account.models import Member


class Training_planStartPageForm(forms.ModelForm):

    excluded_equipment = forms.models.CustomModelMultipleChoiceField(
        queryset=Equipment.objects.all(), required=False)
    # frequenz = forms.ChoiceField(choices=Training_plan.FREQUENZ_CHOICES,
    #                             help_text='Bei einer Zeitspanne von 1 Woche wiederholst du deine Trainingseinheiten nach 7 Tagen.')
    # trainings_count =  forms.IntegerField(
    #                             help_text='Eine Trainingseinheit entspricht einem durchgängigem Training (z.B.: 1 Stunde evtl. mit kurzen Pausen).')
    #frequenz_number =  forms.IntegerField()
    owner = forms.ModelChoiceField(
        queryset=Member.objects.all(), required=False)
    exercise_kinds = forms.models.CustomModelMultipleChoiceField(queryset=Kind.objects.all(),
                                                                 help_text='Denke bei deiner Auswahl auch an die zu empfehlende Auf- bzw. Abwärmphase.', required=False)

    class Meta:
        model = Training_plan
        fields = ('excluded_equipment', 'exercise_kinds', 'owner')

    def save(self, commit=True):

        instance = forms.ModelForm.save(self, True)
        instance.kinds = self.cleaned_data['exercise_kinds']

        # Do we need to save all changes now?

        instance.save()

        return instance


# training_plan °create page 2:
class WarmUpForm(forms.ModelForm):
    exercises = forms.models.CustomModelMultipleChoiceField(
        queryset=Exercise.objects.all(), required=False)
    training = forms.ModelChoiceField(queryset=Training.objects.all())

    class Meta:
        model = WarmUp
        fields = ('exercises', )


class WorkoutForm(forms.ModelForm):
    exercises = forms.models.CustomModelMultipleChoiceField(
        queryset=Exercise.objects.all(), required=False)
    training = forms.ModelChoiceField(
        queryset=Training.objects.all(), required=False)

    class Meta:
        model = Workout
        fields = ('exercises',)


class CoolDownForm(forms.ModelForm):
    exercises = forms.models.CustomModelMultipleChoiceField(
        queryset=Exercise.objects.all(), required=False)
    training = forms.ModelChoiceField(queryset=Training.objects.all())

    class Meta:
        model = CoolDown
        fields = ('exercises', )


class TrainingForm(forms.ModelForm):
    day = forms.IntegerField(required=False)

    class Meta:
        model = Training
        fields = ('duration', 'day')


class IncludedExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(), required=False)

    class Meta:
        model = IncludedExercise
        fields = ('exercise',)


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('weight', 'reversrements', 'duration')


IncludedExerciseFormset = inlineformset_factory(
    IncludedExercise, Set, form=SetForm, can_delete=True, extra=1)


class BaseExercisesFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseExercisesFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = IncludedExerciseFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='exercise-%s-%s' % (
                form.prefix,
                IncludedExerciseFormset.get_default_prefix()))

    def is_valid(self):
        result = True  # super(BaseExercisesFormset, self).is_valid()

        print(self.errors)
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
                    print(form.nested.errors)

        return result

    def save(self, commit=True):

        result = super(BaseExercisesFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


WarmUpExercisesFormset = inlineformset_factory(
    WarmUp, IncludedExercise, form=IncludedExerciseForm, formset=BaseExercisesFormset, exclude=(), extra=3)
CoolDownExercisesFormset = inlineformset_factory(
    CoolDown, IncludedExercise, form=IncludedExerciseForm, formset=BaseExercisesFormset, exclude=(), extra=1)
WorkoutExercisesFormset = inlineformset_factory(
    Workout, IncludedExercise, form=IncludedExerciseForm, formset=BaseExercisesFormset, exclude=(), extra=1)
