from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self): # is automatically called during validation
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 10:
            raise forms.ValidationError('Not enough words! Use at least 10 words.')
        return message # allows modifying the value within validation method, otherwise None will be returned