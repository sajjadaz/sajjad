from django.shortcuts import render, redirect, reverse

from .forms import LoginForm, OtpLoginForm, CheckOtpForm, AddressCreationForm
from django.views import View

from django.contrib.auth import authenticate, login, logout
from .forms import UserEditForm
from random import randint
from .models import Otp, User
from uuid import uuid4
import ghasedakpack

SMS = ghasedakpack.Ghasedak("a053ee8552e377d151c2f8d9a7dcc9431f64828f95eed3d0803f8716ab6748b4")


def user_login(request):
    return render(request, 'account/login.html', {})


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('username', 'اطلاعات وارد شده اشتباه است')
        else:
            form.add_error('username', "طلاعات وارد شده اشتباه است")
        return render(request, 'account/login.html', {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'troshop', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check otp') + f'?token={token}')

        else:
            form.add_error('phone', "طلاعات وارد شده اشتباه است")
        return render(request, 'account/register.html', {'form': form})


class CheckOtpView(View):

    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(username=otp.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return redirect('/')

        else:
            form.add_error('username', "طلاعات وارد شده اشتباه است")
        return render(request, 'account/check_otp.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                form.add_error('username', 'اطلاعات وارد شده اشتباه است')
        else:
            form.add_error('username', "طلاعات وارد شده اشتباه است")
        return render(request, 'account/login.html', {'form': form})


class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def edit_profile(request):
    user = request.user
    form = UserEditForm(instance=user)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)

    if request.method == 'POST':
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'account/edit_profile.html', context={'form': form})




