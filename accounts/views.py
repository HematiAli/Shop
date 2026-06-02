from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, UserAvatarForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import logging


logger = logging.getLogger(__name__)

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        logger.error("register activated")
        return render(request, self.template_name, {'form': self.form_class})
        

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(phone_number=form.cleaned_data['phone'], code=random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session["user_registration_info"] = {#کاربر وقتی اینو تکمیل کرد میفرستمش به صفحه دیگه تا کد رو تایید کنه و این اطلاعات هم نباید بپره برا همین میبرم سشن
                'phone_number':form.cleaned_data['phone'],
                'email':form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        
        return render(request, self.template_name, {'form': form})


class UserRegistrationVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        return render(request, 'accounts/verify.html', {'form': self.form_class})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                          user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registered', 'success')
                return redirect('home:home')
            
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form':form})
    
    
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')
    



class UserPasswordResetView(auth_views.PasswordResetView):#send form by default
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = "accounts/password_reset_email.html"



class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserUploadAvatarView(LoginRequiredMixin, View):
    form_class = UserAvatarForm
    #enctype="multipart/form-data" for upload
    def get(self, request):
        return render(request, 'accounts/avatar.html', {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            messages.success(request, 'avatar saved', 'success')
            return redirect('home:home')
        return render(request, 'accounts/avatar.html', {'form':form})