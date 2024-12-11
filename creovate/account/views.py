from lib2to3.fixes.fix_input import context
from msilib.schema import ListView

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404


from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from django.contrib import messages
from unicodedata import category

from creovate.account.forms import RegisterForm, LoginForm, ResetPasswordForm, PasswordResetConfirmForm, \
    UpdateProfileForm
from creovate.account.models import UserType, Profile

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import views as auth_views, login

from creovate.service.models import Service, ServiceCategory


# Create your views here.


class RegisterViewCustomer(CreateView):
    model = Profile
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'user/register_customer.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        customer_type = get_object_or_404(UserType, id=1)
        user.user_type = customer_type
        user.save()
        return super().form_valid(form)


class RegisterViewFreelancer(CreateView):
    model = Profile
    form_class = RegisterForm
    success_url = reverse_lazy('freelance_homepage')
    template_name = 'user/register_freelancer.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        customer_type = get_object_or_404(UserType, id=2)
        user.user_type = customer_type
        user.save()
        return super().form_valid(form)


class ProfileLoginViewCustomer(LoginView):
    form_class = LoginForm
    template_name = 'user/login_customer.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        if user.user_type and user.user_type.id == 2:
            messages.error(self.request, 'You are not allowed to access this page, Please Login as Freelancer.')
            return HttpResponseRedirect(self.request.path)

        login(self.request, user)
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Email Not Found Or Password Incorrect.')
        return super().form_invalid(form)


    def get_success_url(self):
        return reverse_lazy('home')


class ProfileLoginViewFreelancer(LoginView):
    form_class = LoginForm
    template_name = 'user/login_freelancer.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        if user.user_type and user.user_type.id == 1:
            messages.error(self.request, 'You are not allowed to access this page, Please Login as Customer.')
            return HttpResponseRedirect(self.request.path)
        login(self.request, user)
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Email Not Found Or Password Incorrect.')
        return super().form_invalid(form)


    def get_success_url(self):
        return reverse_lazy('freelance_homepage')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_name = self.request.GET.get('category', 'All')

        if category_name == 'All':
            context['services'] = Service.objects.all()
        else:
            context['services'] = Service.objects.filter(category__name = category_name)

        context['selected_categories'] = category_name
        context['categories'] = ServiceCategory.objects.all()
        return context


class FreelanceHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'common/freelance_homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_name = self.request.GET.get('category', 'All')

        if category_name == 'All':
            service = Service.objects.filter(freelance=self.request.user)
        else:
            service = Service.objects.filter(
                category__name = category_name,
                freelance = self.request.user
            )

        context['services'] = service
        context['selected_categories'] = category_name
        context['categories'] = ServiceCategory.objects.all()

        return context



class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context


class ProfileFreelancePageView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile_freelance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user/customer_update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context

    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse_lazy('profile', kwargs={'username':username})


class UpdateProfileFreelanceView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user/freelance_update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context

    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse_lazy('profile_freelance', kwargs={'username':username})

class ForgotPasswordView(auth_views.PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'resetPassword/forgotPassword.html'


class PasswordResetView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = "resetPassword/passwordReset.html"


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('login')


