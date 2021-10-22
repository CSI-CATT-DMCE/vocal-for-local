import json
from django.core.mail import send_mail
from random import randrange
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from datetime import datetime
# Create your views here.
from django.db import models
from .models import Comment, Customer, Post
from .forms import CreateUserForm
from .forms import CreatePost, ProfileForm

from. forms import states


@login_required(login_url="login")
def home(request):
    posts = Post.objects.all().order_by("-p_id")
    locat = None
    avail = None
    category = None
    profile_filled = True
    try:
        Customer.objects.get(pk=request.user.id)
    except Customer.DoesNotExist:
        profile_filled = False
    if request.method == "POST":
        locat = request.POST['location']
        category = request.POST['category_option']
        avail = request.POST['availability_option']

        # print(category)
        # print(avail)
        # print(locat)

        qs1 = Post.objects.all()
        qs2 = Post.objects.all()
        qs3 = Post.objects.all()
        if(category != '0'):
            qs1 = qs1.filter(category=category)
            # print(qs1)
        if(avail != '0'):
            qs2 = qs2.filter(availability=avail)
            # print(qs2)
        if(locat != '0'):
            # print(states[int(locat)-1])
            qs3 = qs3.filter(location=states[int(locat)-1])
            # print(qs3)
        qs4 = qs1.intersection(qs2, qs3).order_by("-p_id")
        print(qs4)
        return render(request, 'main/home.html', context={'posts': qs4, 'profile_filled': profile_filled})
    return render(request, 'main/home.html', context={'posts': posts, 'profile_filled': profile_filled})


def search(request, key):
    # print(key)
    qs1 = Post.objects.filter(name__contains=key)
    # print(qs1)
    qs2 = Post.objects.filter(description__contains=key)
    # print(qs2)
    qs3 = Post.objects.filter(category=key)

    products_qs = qs1.union(qs2, qs3)
    print(products_qs)

    customer_qs = Customer.objects.filter(business_name__contains=key)
    print([x.business_name for x in customer_qs])

    context = {
        "products_qs": products_qs,
        "customer_qs": customer_qs
    }

    return render(request, 'main/searchResult.html', context)


def about(request):
    return render(request, 'main/about.html', context={})


def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID")
            n = form.cleaned_data["u_name"]
            ph = form.cleaned_data["phone"]
            e = form.cleaned_data["email"]
            st = form.cleaned_data["state"]
            pin = form.cleaned_data["postal_code"]
            ct = form.cleaned_data["city"]
            add = form.cleaned_data["address"]
            b_name = form.cleaned_data["business_name"]
            p = Customer(id=request.user.id, name=n, phone=ph, email=e, state=st,
                         postal_code=pin, city=ct, address=add, business_name=b_name)
            p.save()
            print("SAVED")

        print("hello")
        values = request.POST.getlist('confirmation')
        print(values)
        if len(values) > 0:
            post_id = int(values[0])
            print("{}".format(post_id))
            post = Post.objects.get(p_id=post_id)
            post.delete()
            print("Delete Successful!")

    if(Customer.objects.filter(pk=request.user.id).exists()):
        user_profile = Customer.objects.get(id=request.user.id)
        user_posts = Post.objects.filter(owner=request.user.id)
        init_dict = {
            "u_name": user_profile.name,
            "phone": user_profile.phone,
            "email": request.user.email,
            "business_name": user_profile.business_name,
            "state": user_profile.state,
            "city": user_profile.city,
            "postal_code": user_profile.postal_code,
            "address": user_profile.address,
        }
        form = ProfileForm(initial=init_dict)
        return render(request, 'main/profile.html', context={'form': form, 'user_posts': user_posts, 'user_profile': user_profile})
    form = ProfileForm
    return render(request, 'main/profile.html', context={'form': form})


def upload(request):
    upload_successful = False
    if request.method == "POST":
        form = CreatePost(request.POST or None, request.FILES or None)
        if form.is_valid():
            na = form.cleaned_data["name"]
            note = form.cleaned_data["description"]
            ph = form.cleaned_data["image"]
            ct = form.cleaned_data["category"]
            pr = form.cleaned_data["price"]
            try:
                u = Customer.objects.get(id=request.user.id)
            except Customer.DoesNotExist:
                form = ProfileForm
                return render(request, 'main/profile.html', context={'form': form})
            avail = form.cleaned_data["availability"]
            p = Post(name=na, description=note, owner=u, business_name=u.business_name, date_created=datetime.now(
            ).strftime("%H:%M:%S"), category=ct, photo=ph, availability=avail, location=u.state, price=pr)
            p.save()
            upload_successful = True
    form = CreatePost()
    return render(request, 'main/upload.html', context={'form': form, 'upload_successful': upload_successful})


def registerPage(request):
    if request.method == "POST":

        user = request.POST['username']
        email = request.POST['email']
        pw = request.POST['password']
        print(user)

        if User.objects.filter(username=user).exists():
            messages.info(
                request, "A profile with that username already exists.")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "A profile with that email already exists.")
            return redirect("register")

        else:
            user1 = request.POST['username']

            user = User.objects.create_user(
                username=user, password=pw, email=email)

            user.save()

            messages.success(request, 'Account created for ' + str(user1))
            return redirect("login")

    else:
        return render(request, "main/register.html")


def reset_password(request):
    if request.method == "POST":
        curr_pass = request.POST['new_pass1']
        new_pass = request.POST['new_pass2']
        u1 = request.user.username
        user = authenticate(username=u1)
        if curr_pass == new_pass:
            user = User.objects.get(username=u1)
            user.set_password(new_pass)
            user.save()
            return redirect('login')
        else:
            print("messed up")
            return render(request, 'main/reset_password.html')

    else:
        return render(request, 'main/reset_password.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def delete_post(request):
    post_id = request.GET.get('p_id', False)
    p = Post.objects.get(pk=post_id)
    context = {'post_id': p}
    return render(request, 'main/delete.html', context)


def viewProfile(request, business):
    try:
        c = Customer.objects.get(business_name=business)
    except Customer.DoesNotExist:
        raise Http404("No such Business is currently registered with VFL.")
    posts = Post.objects.filter(owner=c)
    print(c)
    print(posts)
    context = {"c": c, "posts": posts}
    return render(request, 'main/viewProfile.html', context)


def viewPost(request, business, name):
    if request.method == "POST":
        c_text = request.POST["c_text"]
        p_id = Post.objects.get(p_id=request.POST["p_id"])
        c_by = Customer.objects.get(id=request.user.id)
        comment = Comment(text=c_text, p_id=p_id, c_by=c_by)
        comment.save()
        print("Commented!!!")
    try:
        p = Post.objects.filter(business_name=business, name=name)[0]
    except Post.DoesNotExist:
        raise Http404("No such Product is available with {}".format(business))
    comments = Comment.objects.filter(p_id=p).order_by('-c_id')
    context = {"p": p, "comments": comments}
    return render(request, 'main/viewPost.html', context)
