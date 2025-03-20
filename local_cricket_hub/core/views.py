from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm

def home(request):
    return render(request, 'home.html',{'user': request.user})  

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('core:login')
        else:
            print(form.errors)  
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.clubs.exists():
                return redirect('clubs:club_dashboard', club_id=user.clubs.first().id)
            elif user.teams.exists():
                return redirect('teams:team_dashboard', team_id=user.teams.first().id)
            else:
                return redirect('core:dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('core:home')