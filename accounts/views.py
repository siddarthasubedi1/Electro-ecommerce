from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Simple views to render the existing templates.
def register_view(request):    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Now you can login.")
            return redirect(reverse('accounts:loginpage'))
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('store:homepage'))

    if request.method == "POST":
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            
            if not remember_me:
                request.session.set_expire(0)
                
            messages.success(request, 'Logged in successful')
            return redirect(reverse('store:homepage'))
        else:
            messages.error(request, 'Email or Password is invalid')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:loginpage'))

@login_required
def home_view(request):
    return redirect(reverse('base.html'))

def contact_view(request):
	return render(request, 'contact.html')
