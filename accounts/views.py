from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact


def login(request):
    # form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect("login")

    else:
        return render(request, 'accounts/login.html')


def register(request):
    # form submission
    if request.method == 'POST':
        # get form values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # password check
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # unique username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already in use.')
            return redirect('register')

        # unique username
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('register')

        user = User.objects.create(username=username,
                                   email=email,
                                   password=password,
                                   first_name=first_name,
                                   last_name=last_name)
        # login after register
        # auth.login(request, user)
        # messages.success(request, 'You are now logged in.')
        # return redirect('index')

        user.save()
        messages.success(request, 'You are now registered.')
        return redirect('login')

    else:
        return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out.')
        return redirect('index')

    return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)
    context = {'contacts': user_contacts}
    return render(request, 'accounts/dashboard.html', context)
