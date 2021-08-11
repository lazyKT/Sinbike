import urllib
import json

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import UserForm
from .models import FAQ


def signup(request):
    """
    Create Account
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():

            # Google reCAPTCHA
            ''' reCAPTCHA starts '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
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

            if result['success']:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return redirect('common:signup')
    else:
        form = UserForm()

    return render(request, 'common/signup.html', {'form': form})

def faq(request):
    """
    FAQ page
    """
    postlist = FAQ.objects.all()
    return render(request, 'FAQ.html', {'postlist':postlist})
    
def about(request):
    """
    About page
    """
    return render(request, 'about.html')