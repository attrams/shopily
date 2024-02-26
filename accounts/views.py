from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, LoginForm

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)

                return redirect('shop:index')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
