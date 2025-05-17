from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Habit
from .forms import HabitForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def home(request):
    habits = Habit.objects.filter(user=request.user)

    # Add a new habit
    if request.method == 'POST' and 'add_habit' in request.POST:
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('home')
    
    # Update habit status
    elif request.method == 'POST' and 'update_status' in request.POST:
        for habit in habits:
            checkbox_value = request.POST.get(f'habit_{habit.id}')
            habit.is_done_today = bool(checkbox_value)
            habit.save()
        return redirect('home')
    
    else:
        form = HabitForm()

    return render(request, 'tracker/home.html', {'habits': habits, 'form': form})
