from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model # Import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages # For displaying messages
from.forms import UserRegistrationForm # This form needs to be created

# Get the active user model, which is CustomUser in this project
CustomUser = get_user_model()

# --- Helper functions for role-based access ---
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# --- Core Views ---

# 1. User Registration
def register(request):
    if request.user.is_authenticated: # If already logged in, redirect away
        return redirect('events:event_list') # Redirect to event list if already logged in

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves the user, including the selected role
            login(request, user) # Logs the user in immediately after registration
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('events:dashboard') # Redirect to dashboard after successful registration
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm() # Show empty form for GET request
    return render(request, 'accounts/register.html', {'form': form})

# 2. User List (Admin-only)
@login_required # Only allow logged-in users to access
@user_passes_test(is_admin, login_url='/accounts/login/') # Only allow admins
def user_list(request):
    users = CustomUser.objects.all().order_by('username') # Use CustomUser and order them
    return render(request, 'accounts/user_list.html', {'users': users})