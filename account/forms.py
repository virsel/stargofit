from django import forms
from .models import Profile, Member


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class MemberRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email', 'first_name', 'last_name')

   # define clean_<>() method in order to clean the value or raise form validation errors for a field
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.VilidationError('Passwords don\'t match.')
        return cd['password2']


class MemberEditForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('date_of_birth', 'first_name', 'last_name', 'email',
                  'password', 'membername', 'gender')
   # define clean_<>() method in order to clean the value or raise form validation errors for a field

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.VilidationError('Passwords don\'t match.')
        return cd['password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'country')


class MemberOrderForm(forms.Form):
    CHOICES = [
        ('Name', [
            ('membername', 'Membername'),
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
        ]),
        ('date_of_birth', 'Age'),
        ('followers', 'Number of followers'),
    ]

    DIR_CHOICES = [('+', 'Upwards'), ('-', 'Downwards')]

    criteria = forms.ChoiceField(choices=CHOICES)
    direction = forms.ChoiceField(
        choices=DIR_CHOICES, widget=forms.RadioSelect, label='')

    class Meta:
        model = Member


class MemberSearchForm(forms.Form):

    SEARCH_CHOICES = [('membername', 'Membername'), ('get_full_name', 'Full name'),
                      ('first_name', 'First name'), ('last_name', 'Last name')]

    criteria = forms.ChoiceField(choices=SEARCH_CHOICES)
    input = forms.CharField(label='')

    class Meta:
        model = Member
