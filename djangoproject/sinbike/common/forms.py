import urllib
import json

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        # Google reCAPTCHA
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' reCAPTCHA done '''

        if not result['success']:
            raise forms.ValidationError(_('reCAPTCHA error occurred.'))

        return super(UserForm, self).clean()