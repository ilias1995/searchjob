# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.conf import settings


from fillter import ProductFilter
from models import Job, Pravila, JobType
from forms import Reg, Register, UserProfileForm, UpdateProfile




def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return render(request, 'forms/hello.html')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'forms/login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def base(request):
	return render(request, 'forms/base.html')


def job(request):
    f = ProductFilter(request.GET, queryset=Job.objects.all())
    return render(request, 'forms/job.html', {'filter': f })

def jobtypes(request, jobtype_id):
    jobt = JobType.objects.all().order_by('-name')
    jobtype = get_object_or_404(JobType, pk=jobtype_id )
    return render(request, 'forms/jobtypes.html', {'jobt': jobt, 'jobtype': jobtype })

def basejob(request):
    jobtypes = JobType.objects.all()
    return render(request, 'forms/basejob.html', {'jobtypes':jobtypes})

def info(request, id):
	job = Job.objects.get(pk=id)
	return render(request, 'forms/filter.html', {'job': job})

def index(request):
    if request.user.is_authenticated():
        return render(request, 'forms/hello.html')
    else:
    	pravila = Pravila.objects.all
    	return render(request, 'forms/index.html', {'pravila': pravila})

def pravila(request):
    pravila = Pravila.objects.all
    return render(request, 'forms/pravila.html', {'pravila': pravila})


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            return render(request, 'forms/hello.html')
    else:
        form = Register()        
    return render(request, "forms/registeration.html", {'form':form})

def addjob(request,):
    job = Job.objects.all()
    if request.method == 'POST':
        form = Reg(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/')
    else:
        form = Reg()        
    return render(request, "forms/addjob.html", {'form': form, 'job': job})

def profile(request):
    authenticated_user_jobs = Job.objects.filter(user=request.user)
    user_pro = UserProfileForm()
    return render(request, "forms/profile.html", {'user_pro': user_pro, 'job': authenticated_user_jobs})

def delete(request, id):
    authenticated_user_jobs = Job.objects.filter(user=request.user).get(pk=id).delete()
    return render(request, "forms/delete.html", {'job': authenticated_user_jobs})

def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'forms/hello.html')
    else:
        form = UpdateProfile()

    args['form'] = form
    return render(request, 'forms/update_profile.html', args)

def change_success(request):
    return render(request, 'forms/change_success.html')

def password_change(request,
                    template_name='forms/change_password.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/forms/change_success')
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': ('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template_name, context,
                            current_app=current_app)

def password_reset(request, is_admin_site=False,
                   template_name='forms/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        pass
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect('/forms/password_reset_done/')
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': ('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_done(request,
                        template_name='forms/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': ('Password reset successful'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL

def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='forms/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        pass
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = ('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = ('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': ('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)