# Create your views here.

import os
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from wtpixel.forms import ImageForm, SignUpForm, LoginForm, VideoForm, MusicForm
from django.contrib import messages
from wtpixel.models import Image, Video, Music
import nude


def index(request):
    portfolio = Image.objects.all().order_by('-uploaded_at')
    context = {"portfolios": portfolio}
    return render(request, "index.html", context)


def sitemap(request):
    return render(request, "sitemap.xml")


@login_required(login_url="/login/")
def dashb(request):
    if request.method == 'POST':
        pic_id = int(request.POST.get("pic_id"))
        status = str(request.POST.get("status"))
        sts = Image.objects.get(id=pic_id)
        sts.status = status
        sts.save()
    portfolio = Image.objects.all()
    context = {"portfolios": portfolio}
    return render(request, "dashb/index.html", context)


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
                if request.user.is_superuser:
                    return redirect('/dashb')
                return redirect("/")

            else:
                msg = "Username or Password Doesn't match"

        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    us = User.objects.filter(username=user)
    image = Image.objects.filter(user=user)
    video = Video.objects.filter(user=user)
    music = Music.objects.filter(user=user)
    return render(request, 'profile.html', {'profile': us, 'image': image, 'video': video, 'music': music})


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


def save_views(req):
    if req.method == "GET":
        pk = req.GET.get("obj")
        obj = Image.objects.get(pk=pk)
        obj.views += 1
        obj.save()

        print("inside save view")

        return JsonResponse({'status': obj.views})
    pass


def save_video_views(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Video.objects.get(pk=pk)
        obj.views += 1
        obj.save()

        print("inside save view")

        return JsonResponse({'status': obj.views})
    pass


def music_views(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Music.objects.get(pk=pk)
        obj.views += 1
        obj.save()

    print("inside save view")

    return JsonResponse({'status': obj.views})
    pass


@csrf_exempt
def count_likes(req):
    if req.method == 'POST':
        print("inside")
        post = get_object_or_404(Image, id=req.POST.get("id"))
        print(req.POST.get("id"))

        liked = False
        if post.likes.filter(id=req.user.id).exists():
            post.likes.remove(req.user)

        else:
            liked = True
            post.likes.add(req.user)

        total_likes = post.number_of_liked;
        print(total_likes)
        print("end view")
        print(req.user)
        return JsonResponse({'liked': liked, 'total_likes': total_likes, 'id': str(req.POST.get("id"))})
    pass


def save_music_view(req):
    if req.method == 'GET':
        pk = req.GET.get("obj")
        obj = Music.objects.get(pk=pk)
        obj.views += 1
        obj.save()
        print('inside music views')
        return JsonResponse({'status': obj.views})
    pass


def count_downloads(req):
    if req.method == "GET":
        pk = req.GET.get("obj")
        obj = Image.objects.get(pk=pk)
        obj.total_downloads += 1
        obj.save()

        print("inside save view")

    return JsonResponse({'status': obj.total_downloads})


@login_required(login_url="/login/")
def upload(request):
    if request.method == 'POST':
        image = ImageForm(request.POST, request.FILES)
        video = VideoForm(request.POST, request.FILES)
        music = MusicForm(request.POST, request.FILES)

        ext = os.path.splitext(str(request.FILES['file']))[-1].lower()
        print(ext)

        if ext == ".mp4":
            print("mp4 file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Video successfully Uploaded.')

                return redirect('upload')

        elif ext == ".mkv":
            print("mkv file!")

            if video.is_valid:
                # form.save()
                fs = video.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Video successfully Uploaded.')

                return redirect('upload')

        elif ext == ".mp3":
            print("mp3 file!")

            if music.is_valid:
                # form.save()
                fs = music.save(commit=False)
                fs.user = request.user
                fs.save()
                messages.success(request, 'Music Successfully Uploaded.')

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
                messages.success(request, 'Image Successfully Uploaded.')

                return redirect('upload')

        else:
            print("Unknown file format.")
            messages.warning(request, 'Unknown File Format !!')

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
        object_list = Image.objects.filter(Q(title__icontains=query) | Q(file__icontains=query))
        print(object_list)
        return object_list


def read_file(request):
    f = open('.well-known/pki-validation/15782C901DF587AE2A25B2170549D1D0.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
