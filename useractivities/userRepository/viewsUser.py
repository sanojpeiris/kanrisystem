from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from useractivities.filters import TaskFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# from useractivities.userRepository.models import TaskItem


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username = email, password=password)
               
        if user is None:
            messages.info(request, "invalid information")
            return redirect("/")
        else:
            if user.last_login is None:
                auth.login(request, user)
                return redirect(homeAlert)
            else:
                auth.login(request, user)
                return redirect(moveToHome)
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return render(request, "login.html")


def moveToRegister(request):
    return render(request, "register.html")


def register(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        is_admin = request.POST.get('is_admin', False)

        if password1 == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email exists")
                return redirect("register")
            else:
                if is_admin:
                    user = User.objects.create_superuser(username=username,
                                                         email=email,
                                                         password=password1,
                                                         )
                    user.save()
                    messages.info(request, "successfully created the Admin user")
                    return redirect("/")

                else:
                    if password1 == password2:
                        if User.objects.filter(username=username).exists():
                            messages.info(request, "Username already taken")
                            return redirect("register")
                        elif User.objects.filter(email=email).exists():
                            messages.info(request, "email exists")
                            return redirect("register")

                        else:
                            user = User.objects.create_user(username=username,
                                                            email=email,
                                                            password=password1)
                            user.save()
                            messages.info(request, "successfully created the Regular user")
                            return redirect("/")
    else:
        messages.info(request, "password is not match")
        return redirect("/")


def updateUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if email == request.user.email:
                user = User.objects.get(username=username)
                user.email = email
                user.save()

                password = User.objects.get(username=username)
                password.set_password(password1)
                password.save()

                messages.info(request, "password changed")
                return redirect("moveToUpdateUser")
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "email exists")
                    return redirect("moveToUpdateUser")

                user = User.objects.get(username=username)
                user.email = email
                user.save()

                password = User.objects.get(username=username)
                password.set_password(password1)
                password.save()

                messages.info(request, "password changed")
                return redirect("moveToUpdateUser")
        else:
            messages.info(request, "password is not match")
            return redirect("moveToUpdateUser")
    else:
        return render(request, "login.html")


def moveToUpdatePassword(request):
    return render(request, "updatePassword.html")


def updatePassword(request):
    if request.method == "POST":
        userId = request.user.id
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            password = User.objects.get(id=userId)
            password.set_password(password1)
            password.save()

            messages.info(request, "password changed")
            return redirect(closeWindow)
        else:
            messages.info(request, "password is not match")
            return redirect(moveToUpdateUser)
    else:
        return render(request, "login.html")


def moveToUpdateUser(request):
    return render(request, "updateUser.html")


def closeWindow(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def homeAlert(request):
    first_login = True
    return render(request, "home.html", {"first_login": first_login})


def moveToHome(request):
    return redirect("taskView")
