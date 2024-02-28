from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm

from .forms import SignUpForm, LoginForm, PasswordResetRequestForm
from .tasks import send_confirmation_email, send_password_reset

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'shop:index')
        return redirect(next_url)

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

                    # Redirect to the 'next' parameter if it exists, else default to 'shop:index'
                    next_url = request.POST.get(
                        'next') or request.GET.get('next', 'shop:index')
                    return redirect(next_url)

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

    return render(request, 'accounts/login.html', {'form': form, 'next': request.GET.get('next', '')})


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


def forgot_password(request):
    User = get_user_model()

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)

                current_site = get_current_site(request)

                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'site_name': 'shopily',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })

                if user.is_active:

                    send_password_reset.delay(user.pk, message)

                    messages.success(
                        request=request,
                        message='Password reset instructions sent. Please check your email.'
                    )

                else:
                    messages.error(
                        request=request,
                        message='Your account is inactive. Please contact support.'
                    )

            except User.DoesNotExist:
                messages.info(
                    request=request,
                    message='No user is associated with this email address.'
                )

    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})


def password_reset(request, uidb64, token):
    '''
    This allows users who forgot their password to change their password.
    '''

    if request.user.is_authenticated:
        return redirect('shop:index')

    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        messages.error(
            request=request,
            message='It looks like your account got deleted. Please create a new one.'
        )
        return redirect('accounts:signup')

    if request.method == 'POST':
        # process the password reset form submission
        form = SetPasswordForm(user, request.POST)

        # prevent inactive users from resetting password
        if form.is_valid():

            if user.is_active:
                new_password = form.cleaned_data['new_password1']

                # check if new password is not the same as the old password
                if user.check_password(new_password):
                    messages.error(
                        request=request,
                        message='Your new password cannot be the same as your old password.'
                    )
                    return render(request, 'accounts/password_reset.html', {'form': form})

                form.save()
                messages.success(
                    request=request,
                    message='Your password has been reset successfully. You can now log in with your new password.'
                )

            else:
                messages.error(
                    request=request,
                    message='Password reset failed because your account is inactive. Please contact support.'
                )

            return redirect('accounts:login')

        else:
            return render(request, 'accounts/password_reset.html', {'form': form})

    elif request.method == 'GET':
        if user is not None and default_token_generator.check_token(user, token):
            # A form that lets a user change their password without entering the old password.
            form = SetPasswordForm(user)

            return render(request, 'accounts/password_reset.html', {'form': form})

        else:
            messages.error(
                request=request,
                message='The password reset link is invalid or expired. Please request a new one.'
            )

            return redirect('accounts:forgot_password')
