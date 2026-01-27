from django.shortcuts import render


# Simple views to render the existing templates.
def login_view(request):
	return render(request, 'login.html')


def register_view(request):
	return render(request, 'register.html')


def contact_view(request):
	return render(request, 'contact.html')
