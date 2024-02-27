from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import SignUpForm, LoginForm
from .tasks import send_confirmation_email

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

                if user.is_active:
                    login(request, user)

                    return redirect('shop:index')

                else:
                    messages.info(
                        request=request,
                        message='Your account is inactive. Please contact support.'
                    )

            else:
                messages.error(
                    request=request,
                    message='Incorrect username/email or password.'
                )

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)

    return redirect('shop:index')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # send confirmation email
            current_site = get_current_site(request)
            message = render_to_string('accounts/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            send_confirmation_email.delay(user.pk, message)
            messages.success(
                request=request,
                message='Your account has been created successfully! Please check your email on how to activate your account.'
            )

            return redirect('accounts:login')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request,
            message='Your account has been activated!'
        )

        return redirect('accounts:login')

    else:
        messages.error(
            request=request,
            message='An error occured while activating your account. Please contact adminstration'
        )

        return redirect('accounts:login')
