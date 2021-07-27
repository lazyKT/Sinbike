from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import FAQ


def signup(request):
    """
    Create Account
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def faq(request):
    """
    FAQ page
    """
    postlist = FAQ.objects.all()
    return render(request, 'FAQ.html', {'postlist':postlist})
    
