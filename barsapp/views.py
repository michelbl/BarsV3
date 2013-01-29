#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import auth
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from myform.models import LoginForm
from barsapp.models import *
from barsapp import settings

def _authentication(request, context):
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return True
                else:
                    # Return a 'disabled account' error message
                    context['login_error'] = 'Compte désactivé.'
                    return False
        # Return an 'invalid login' error message.
        context['login_error'] = u'Login ou mot de passe incorrect.'
    return False

def _load_context(request):
    context = {
        'base_url': settings.BASE_URL,
        'version': settings.VERSION,
        'bar_list': Bar.objects.all(),
        'mail_babe': settings.MAIL,
        }
    return context
 

def index(request):
    t = loader.get_template('barsapp/base_choix.html')
    context = _load_context(request)
    _authentication(request, context)
    if request.user.is_authenticated():
        context['my_user'] = {
            'pseudo': request.user.get_full_name(),
            'id': request.user.pk,
            'bar_list': [baruser.bar for baruser in
                BarsUser.objects.filter(user=request.user)]
            }
    else:
        context['login_form'] = LoginForm()
        try:
            remote_ip = IP.objects.get(ip=request.META['REMOTE_ADDR'])
        except ObjectDoesNotExist:
            pass
        else:
            if remote_ip.sort:
                context['my_ip'] = {'bar': remote_ip.bar,}
            else:
                context['my_ip'] = {
                    'user': remote_ip.user.get_full_name(),
                    'bar_list': [baruser.bar for baruser in
                        BarsUser.objects.filter(user=remote_ip.user)]
                    }
 
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def logout(request, bar_name=''):
    auth.logout(request)
    if bar_name != '':
        return redirect('/' + bar_name + '/')
    else:
        return redirect('/')


def bar_home(request, bar_name):
    bar = get_object_or_404 (Bar, name=bar_name)
    t = loader.get_template('barsapp/base_bar.html')
    context = _load_context(request)
    context['bar']=bar
    _authentication(request, context)
    if request.user.is_authenticated():
        try:
            my_barsuser = BarsUser.objects.get(bar=bar, user=request.user)
        except ObjectDoesNotExist:
            context['my_user'] = {
                'pseudo': request.user.get_full_name(),
                'id': request.user.pk,
                'known': False,
                }
        else:
            context['my_user'] = {
                'pseudo': request.user.get_full_name(),
                'id': request.user.pk,
                'known': True,
                'respo': my_barsuser.respo,
                'amount': my_barsuser.credit,
                'bar_list': [baruser.bar for baruser in
                    BarsUser.objects.filter(user=request.user)]
                }
    else:
        context['login_form'] = LoginForm()
        try:
            remote_ip = IP.objects.get(ip=request.META['REMOTE_ADDR'])
        except ObjectDoesNotExist:
            pass
        else:
            if remote_ip.sort:
                context['my_ip'] = {'bar': remote_ip.bar,}
            else:
                context['my_ip'] = {
                    'user': remote_ip.user.get_full_name(),
                    'bar_list': [baruser.bar for baruser in
                        BarsUser.objects.filter(user=remote_ip.user)]
                    }
 
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))




















def login(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('barsapp/login.html',
            {'error' : error, 'form' : form,},
            context_instance=RequestContext(request))

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    auth.login(request, user)
                    return HttpResponseRedirect('/secured/')
                else:
                    # Return a 'disabled account' error message
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                # Return an 'invalid login' error message.
                error = u'invalid login'
                return errorHandle(error)
        else: 
            error = u'form is invalid'
            return errorHandle(error)		
    else:
        form = LoginForm() # An unbound form
        return render_to_response('barsapp/login.html', {'form': form,},
            context_instance=RequestContext(request))

def secured(request):
    if request.user.is_authenticated():
        return render_to_response('barsapp/secured.html',
            {'username': request.user.username,})
    else:
        return redirect('login')

def wrong(request):
    return redirect('login')
