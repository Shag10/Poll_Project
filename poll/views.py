from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CreatePollForm
from .models import Poll
from django.contrib.auth.models import User, auth

def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'poll/index.html', context)
@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username = name, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'Invalid user')
            return redirect("login")
    else:
        context = {
        'login' : login
    }
        return render(request, 'poll/login.html', context)

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = name).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:    
                user = User.objects.create_user(username = name, email = email, password = password1)
                user.save()
                messages.info(request, 'User created')
        else:
            messages.info(request, 'Password does not match')
            return redirect('register')
        return redirect('home')
    else:
        context = {
        'register' : register
    }
        return render(request, 'poll/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')