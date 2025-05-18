from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from .models import Habit, HabitStatus
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
    today = date.today()
    days = [today.replace(day=1) + timedelta(days=i) for i in range(31) if (today.replace(day=1) + timedelta(days=i)).month == today.month]

    if request.method == 'POST':
        if 'delete_habit' in request.POST:
            habit_id = request.POST.get('delete_habit')
            Habit.objects.filter(id=habit_id, user=request.user).delete()
            return redirect('home')

        elif 'add_habit' in request.POST:
            form = HabitForm(request.POST)
            if form.is_valid():
                habit = form.save(commit=False)
                habit.user = request.user
                habit.save()
                return redirect('home')

        elif 'update_status' in request.POST:
            for habit in habits:
                for d in days:
                    checkbox_name = f"{habit.id}_{d.strftime('%Y-%m-%d')}"
                    is_checked = checkbox_name in request.POST

                    obj, _ = HabitStatus.objects.get_or_create(habit=habit, date=d)
                    obj.is_done = is_checked
                    obj.save()
            return redirect('home')
    else:
        form = HabitForm()

    status = {}
    for habit in habits:
        status[habit.id] = {s.date.strftime('%Y-%m-%d'): s.is_done for s in HabitStatus.objects.filter(habit=habit, date__in=days)}

    return render(request, 'tracker/home.html', {'habits': habits, 'form': form, 'days': days, 'status': status})