from decimal import Decimal
from lib2to3.fixes.fix_input import context
from msilib.schema import ListView

from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy

from django.utils.timezone import now
from datetime import timedelta

from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from unicodedata import category

from creovate.account.forms import RegisterForm, LoginForm, ResetPasswordForm, PasswordResetConfirmForm, \
    UpdateProfileForm, UpdateWalletForm
from creovate.account.models import UserType, Profile, Wallet, Order

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth import views as auth_views, login

from creovate.service.models import Service, ServiceCategory
from django.db import transaction

from django.core.mail import send_mail
from django.core.paginator import Paginator


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

        customer_permission = Permission.objects.get(codename='can_access_customer_page')
        customer_delete_permission = Permission.objects.get(codename='can_delete_customer_page')

        user.user_permissions.add(customer_permission)
        user.user_permissions.add(customer_delete_permission)

        Wallet.objects.create(profile=user)
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

        freelancer_permission = Permission.objects.get(codename='can_access_freelancer_page')
        freelancer_delete_permission = Permission.objects.get(codename='can_delete_freelancer_page')

        user.user_permissions.add(freelancer_permission)
        user.user_permissions.add(freelancer_delete_permission)

        Wallet.objects.create(profile=user)
        messages.success(self.request, 'Your account has been created.')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Error when creating your account.')
        return super().form_invalid(form)


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


class HomeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'common/home.html'
    permission_required = 'account.can_access_customer_page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q', '')
        category_name = self.request.GET.get('category', 'All')

        services = Service.objects.all()
        if category_name != 'All':
            services = services.filter(category__name=category_name)

        if search_query:
            services = services.filter(title__icontains=search_query)

        context['services'] = services
        context['selected_categories'] = category_name
        context['categories'] = ServiceCategory.objects.all()
        context['search_query'] = search_query  # Simpan untuk menampilkan ulang input
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class FreelanceHomeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'common/freelancer_homepage.html'
    permission_required = 'account.can_access_freelancer_page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Dapatkan query pencarian
        search_query = self.request.GET.get('q', '')
        category_name = self.request.GET.get('category', 'All')

        # Filter layanan berdasarkan kategori dan judul
        services = Service.objects.filter(freelance=self.request.user)
        if category_name != 'All':
            services = services.filter(category__name=category_name)

        if search_query:
            services = services.filter(title__icontains=search_query)

        context['services'] = services
        context['selected_categories'] = category_name
        context['categories'] = ServiceCategory.objects.all()
        context['search_query'] = search_query  # Untuk menampilkan ulang input pencarian
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')



class ProfilePageView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'user/profile_customer.html'
    permission_required = 'account.can_access_customer_page'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class ProfileFreelancePageView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'user/profile_freelancer.html'
    permission_required = 'account.can_access_freelancer_page'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')

class UpdateProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user/customer_update_profile.html'
    permission_required = 'account.can_access_customer_page'



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


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class UpdateProfileFreelanceView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'user/freelancer_update_profile.html'
    permission_required = 'account.can_access_freelancer_page'



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


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')

class ForgotPasswordView(auth_views.PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'resetPassword/forgotPassword.html'


class PasswordResetView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = "resetPassword/passwordReset.html"


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('login')


class WalletViewCustomer(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Wallet
    context_object_name = 'wallet'
    template_name = 'user/wallet_customer.html'
    permission_required = 'account.can_access_customer_page'


    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        if not wallet or profile.username != request.user.username:
            return redirect('error')

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        context['wallet'] = wallet
        context['username'] = username
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class WalletViewFreelancer(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Wallet
    context_object_name = 'wallet'
    template_name = 'user/wallet_freelancer.html'
    permission_required = 'account.can_access_freelancer_page'


    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        if not wallet or profile.username != request.user.username:
            return redirect('error')

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        context['wallet'] = wallet
        context['username'] = username
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')


class UpdateWalletViewCustomer(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Wallet
    form_class = UpdateWalletForm
    context_object_name = 'wallet'
    template_name = 'user/update_wallet_customer.html'
    permission_required = 'account.can_access_customer_page'


    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        if not wallet or profile.username != request.user.username:
            return redirect('error')

        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        return self.request.user


    @transaction.atomic
    def form_valid(self, form):
        try:
            wallet = Wallet.objects.get(profile=self.request.user)
            additional_balance = Decimal(form.cleaned_data['balance'])
            wallet.balance += additional_balance
            wallet.save()

        except Exception as e:
            transaction.set_rollback(True)
            raise e

        return super().form_valid(form)


    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse_lazy('customer_wallet', kwargs={'username':username})


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class UpdateWalletViewFreelancer(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Wallet
    form_class = UpdateWalletForm
    context_object_name = 'wallet'
    template_name = 'user/update_wallet_customer.html'
    permission_required = 'account.can_access_freelancer_page'


    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        profile = Profile.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(profile=profile).first() if profile else None

        if not wallet or profile.username != request.user.username:
            return redirect('error')

        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        return self.request.user


    @transaction.atomic
    def form_valid(self, form):
        try:
            wallet = Wallet.objects.get(profile=self.request.user)
            additional_balance = Decimal(form.cleaned_data['balance'])
            wallet.balance += additional_balance
            wallet.save()

        except Exception as e:
            transaction.set_rollback(True)
            raise e

        return super().form_valid(form)


    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse_lazy('freelancer_wallet', kwargs={'username':username})


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')


class CheckOutView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'account.can_access_customer_page'


    def post(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        description = request.POST.get('description', '')

        try:
            with transaction.atomic():
                customer = Wallet.objects.select_for_update().get(profile=request.user)
                freelancer = Wallet.objects.select_for_update().get(profile=service.freelance.id)

                if customer.balance < service.price:
                    messages.error(request, 'Insufficient Balance!')
                    return redirect('service', slug=service.slug)

                customer.balance -= service.price
                freelancer.balance += service.price
                customer.save()
                freelancer.save()

                Order.objects.create(
                    profile=request.user,
                    service=service,
                    description=description
                )

                send_mail(
                    subject=f'New Order🚨: {service.title}',
                    message=f'Hi {service.freelance.username}👋,\n\n'
                            f'We’re excited to inform you that {request.user.username} has purchased your service🎉. Here are the details of the transaction:\n\n'
                            f'Service Description: {description}\n\n'
                            f'Price: Rp.{service.price}\n'
                            f'To discuss project specifics, feel free to connect with the customer via email at {request.user.email}\n'                            
                            f'Thank you for being an integral part of Creovate! Your creativity and dedication inspire us every day. Keep up the fantastic work! 🚀🔥\n\n'
                            'Best regards\n'
                            'Creovate Team',
                    from_email=f'{request.user.email}',
                    recipient_list=[service.freelance.email],
                )

            messages.success(request, 'Checkout Success!')
            return redirect('service', slug=service.slug)

        except Exception as e:
            messages.error(request, e)
            return redirect('service', slug=service.slug)


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')



class HistoryView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Order
    template_name = 'user/customer_history_order.html'
    permission_required = 'account.can_access_customer_page'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        user = self.request.user
        orders = Order.objects.filter(profile=user).order_by('-order_date')

        paginator = Paginator(orders, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['user_order'] = page_obj
        context['page_obj'] = page_obj

        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class CancelOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'account.can_access_customer_page'

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, profile=request.user)
        elapsed_time = now() - order.order_date

        if elapsed_time > timedelta(days=1):
            messages.error(request, 'Purchase cannot be cancelled after 24 hours!')
            return redirect('history_order', username=request.user.username)

        try:
            with transaction.atomic():
                customer = Wallet.objects.select_for_update().get(profile=request.user)
                freelancer = Wallet.objects.select_for_update().get(profile=order.service.freelance.id)

                customer.balance += order.service.price
                freelancer.balance -= order.service.price
                customer.save()
                freelancer.save()

                send_mail(
                    subject=f'Order Cancellation Notification 🚨: {order.service.title}',
                    message = (f'Hello {order.service.freelance.username},\n\n'
                           f'We hope this message finds you well. We want to inform you that {request.user.username} has decided to cancel their purchase of your "{order.service.title}" service.\n\n'
                           f'While cancellations can be disappointing, please know that Creovate values your creativity and commitment to delivering outstanding services. Keep up the great work, and we look forward to supporting your journey as a talented freelancer! 🔥\n\n'
                           'Warm regards,\n'
                           'The Creovate Team'),
                    from_email=f'{request.user.email}',
                    recipient_list=[order.service.freelance.email],
                )

                messages.success(request, 'Successfully canceled your purchase!')
                order.delete()
                return redirect('history_order', username=request.user.username)

        except Exception as e:
            messages.error(request, "Error while cancelling your purchase!, Please try again")
            return redirect('history_order', username=request.user.username)


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class OrderListFreelancerView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Order
    template_name = 'user/freelancer_order_list.html'
    permission_required = 'account.can_access_freelancer_page'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username
        user = self.request.user
        orders = Order.objects.filter(service__freelance=user).order_by('-order_date')

        paginator = Paginator(orders, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['user_order'] = page_obj
        context['page_obj'] = page_obj

        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')


class DetailOrderListView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'user/freelancer_order_detail.html'
    permission_required = 'account.can_access_freelancer_page'


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.service.freelance != request.user:
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_instance = self.object.service
        context['related_orders'] = Order.objects.filter(service=service_instance)
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')