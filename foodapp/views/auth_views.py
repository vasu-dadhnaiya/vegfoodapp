from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foodapp.forms import ProfileForm

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not full_name or not email or not password:
            messages.error(request, "All fields are required.")
        elif User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to VegFood, {user.first_name}!")
            return redirect('home')
            
    return render(request, 'accounts/auth.html', {'active_tab': 'register'})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard_home')
        return redirect('home')
        
    next_url = request.GET.get('next', '')
    if not next_url:
        next_url = request.POST.get('next', '')
        
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=email, password=password)
        if user is None:
            # Try finding user by email
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if next_url:
                return redirect(next_url)
            if user.is_superuser:
                return redirect('dashboard_home')
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            
    return render(request, 'accounts/auth.html', {'active_tab': 'login', 'next': next_url})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors in your profile form.")
    else:
        form = ProfileForm(instance=request.user)
            
    return render(request, 'accounts/profile.html', {'form': form})
