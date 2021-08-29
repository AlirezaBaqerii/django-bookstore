from django.shortcuts import redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .token import account_activation_token
from .models import BaseUser


@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html',)
    # {'section': 'profile', 'orders': orders})

def account_register(request):
    # if request.user.is_authenticated: # age login bashe redirect mishe
    #     return redirect('/')
    
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST) # getting data from post
        print('furst if')
        if registrationForm.is_valid():
            print('second jif')
            user = registrationForm.save(commit=False)
            user.email = registrationForm.cleaned_data['email']
            user.set_password(registrationForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = 'Activate your email'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
        return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = BaseUser.objects.get(pk=uid)  
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/registration/activation_invalid.html')
    except:
        pass