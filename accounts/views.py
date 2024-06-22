
from django.contrib.auth.views import PasswordChangeView
from .forms import ChangePasswordForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UsserRegistrationForm, UserUpdateForm
from django.contrib.auth import login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages

def send_mail(user, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html' 
    form_class = UsserRegistrationForm
    success_url = reverse_lazy('register')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(request, *args, **kwargs)
    

    def get_success_url(self):
        return reverse_lazy('home')
    

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login')  
    template_name = 'accounts/change_password.html'  
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        message = 'Password changed'

        send_mail(self.request.user, message, 'accounts/password_change_success.html')

        messages.success(self.request, 'Your password was changed successfully.')

        return response