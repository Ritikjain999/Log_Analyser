from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from django.conf import settings
from .forms import LogFileUploadForm
import os

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")

    if request.method == "POST":
        form = LogFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            log_file = form.cleaned_data['log_file']
            log_file_dir = os.path.join(settings.MEDIA_ROOT, 'log_file')
            os.makedirs(log_file_dir, exist_ok=True)
            log_file_path = os.path.join(log_file_dir, log_file.name)
            if log_file.name.endswith(".log"):
                with open(log_file_path, 'wb+') as destination:
                    for chunk in log_file.chunks():
                        destination.write(chunk)
                ERRORS = parse_log_file(log_file_path)
                if len(ERRORS) != 0:
                    return render(request, 'upload_success.html', {'file_name': log_file.name, 'error': ERRORS})
                return render(request, 'upload_success.html', {'file_name': log_file.name, 'error': "NO ERROR FOUND!!!"})
            else:
                return render(request, 'upload_unsuccessful.html', {'file_name': log_file.name})

    form = LogFileUploadForm()
    return render(request, 'index.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("/login")


def parse_log_file(log_file_path):
    new_lines = []
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if line.find("ERROR"):
                new_lines.append(line)
                if len(new_lines) == 10:
                    break
    return new_lines

