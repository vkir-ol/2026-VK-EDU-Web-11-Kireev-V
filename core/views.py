from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ProfileForm

def signup(request):
    form = SignupForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(user=request.user)

    return render(request, 'core/profile.html', {'form': form})
