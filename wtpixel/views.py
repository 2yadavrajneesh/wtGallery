# Create your views here.

import json
import os
from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from wtpixel.forms import ImageForm, SignUpForm, LoginForm, VideoForm, MusicForm
from django.contrib import messages
from wtpixel.models import Image, Video, Music
import nude


# def index(request):
#     portfolio = Image.objects.all()
#     context = {"portfolio": portfolio}
#     return render(request, "index.html", context)

class IndexView(ListView):
    model = Image
    paginate_by = 10
    context_object_name = 'portfolios'
    template_name = 'index.html'
    ordering = ['title']


def profile(request, username):
    user = get_object_or_404(User, username=username)
    us = User.objects.filter(username = user)
    return render(request, 'dashboard.html', {'profile': us})


def image(request):
    portfolio = Image.objects.all()
    context = {"portfolio": portfolio}
    return render(request, "images.html", context)


def video(request):
    portfolio = Video.objects.all()
    context = {"portfolio": portfolio}
    return render(request, "video.html", context)


def music(request):
    portfolio = Music.objects.all()
    print(portfolio)
    context = {"portfolio": portfolio}
    return render(request, "music.html", context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "register.html", {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Username or Password Doesn't match"

        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})


@login_required(login_url="/login/")
def upload(request):
    if request.method == 'POST':
        image = ImageForm(request.POST, request.FILES)
        video = VideoForm(request.POST, request.FILES)
        music = MusicForm(request.POST, request.FILES)

        # Split the extension from the path and normalise it to lowercase.
        ext = os.path.splitext(str(request.FILES['file']))[-1].lower()
        print(ext)

        # Now we can simply use == to check for equality, no need for wildcards.

        if ext == ".mp4":
            print("mp4 file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Video inserted successfully.')

                return redirect('upload')

        elif ext == ".mkv":
            print("mkv file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Video inserted successfully.')

                return redirect('upload')

        elif ext == ".mp3":
            print("mp3 file!")

            if music.is_valid:
                # form.save()
                fs = music.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Music inserted successfully.')

                return redirect('upload')

        elif ext == ".png" or ".jpg" or ".jpeg":
            print("image file!")

            if image.is_valid():
                # if nude.is_nude(request.FILES['file']):
                #     messages.warning(request, 'Inappropriate image detected, This is against our company policy !!')
                # else:
                    # form.save()
                fs = image.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Image inserted successfully.')

                return redirect('upload')

        else:
            print("Unknown file format.")
            messages.warning(request, 'Unknown file format !!')

        # if image.is_valid() or video.is_valid:
        #
        #     if nude.is_nude(request.FILES['image']):
        #         messages.warning(request, 'Inappropriate image detected, This is against our company policy !!')
        #     else:
        #         # form.save()
        #         fs = image.save(commit=False)
        #         fs.user = request.user
        #         fs.save()
        #         messages.success(request, 'Image inserted successfully.')
        #
        #     return redirect('upload')
    else:
        form = ImageForm() or VideoForm()
    return render(request, 'upload.html', {'form': form})


class SearchResultsView(ListView):
    model = Image
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Image.objects.filter(Q(title__icontains=query) | Q(file__icontains=query) )
        print(object_list)
        return object_list


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))
