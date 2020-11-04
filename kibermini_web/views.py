from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from kibermini_nodes.models import Location
from kibermini_nodes import tasks


def index(request):
    return render(request, 'index.html', {"user": request.user})


def sign_in(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return redirect("index")
    return render(request, 'sign_in.html', {"user": request.user})


def sign_up(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("panel")

        return render(request, "sign_up.html", {"user": request.user, 'form': form})
    else:
        form = UserCreationForm()
        return render(request, "sign_up.html", {"user": request.user, 'form': form})


def logout_view(request):
    logout(request)
    return redirect("index")


def panel(request):
    if request.user.is_authenticated:
        if request.is_ajax() and request.POST:
            pass
        if request.POST:
            result = tasks.manager_task(request.user.id, request.POST["time"],
                                  request.POST["period"], request.POST["location"],
                                  request.POST["computer"])

            return render(request, "panel.html",
                          {"user": request.user, "locations": Location.objects.all(), "result": result})
        else:
            return render(request, "panel.html", {"user": request.user, "locations": Location.objects.all()})
    else:
        return redirect("sign_in")
