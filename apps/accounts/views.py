from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.core.permissions import role_required

from .forms import UserCreateForm
from .models import Role, User


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"user_obj": request.user})


@role_required(Role.ADMIN)
def user_list(request):
    users = User.objects.order_by("full_name")
    return render(request, "accounts/user_list.html", {"users": users})


@role_required(Role.ADMIN)
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.email} created.")
            return redirect("accounts:user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_form.html", {"form": form})
