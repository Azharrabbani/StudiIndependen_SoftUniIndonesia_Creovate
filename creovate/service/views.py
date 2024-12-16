from lib2to3.fixes.fix_input import context

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import HttpResponseForbidden, Http404
from django.contrib import messages


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView

from creovate.service.forms import AddServiceForm, UpdateServiceForm
from creovate.service.models import Service


# Create your views here.
class DetailServiceView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'service/service_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'account.can_access_customer_page'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category = self.object.category
        context['filtered_services'] = Service.objects.filter(category=current_category).exclude(id=self.object.id)
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('login')


class AddServiceView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Service
    form_class = AddServiceForm
    success_url = reverse_lazy('freelance_homepage')
    template_name = 'service/add_service.html'
    permission_required = "account.can_access_freelancer_page"

    def form_valid(self, form):
        service = form.save(commit=False)
        service.freelance = self.request.user
        service.save()
        messages.success(self.request, 'Hooray you have added a service🤩!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')

class UpdateServiceView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = UpdateServiceForm
    context_object_name = 'service'
    success_url = reverse_lazy('freelance_homepage')
    template_name = 'service/update_service.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'account.can_access_freelancer_page'

    def dispatch(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            return redirect('error')

        if obj.freelance != request.user:
            return redirect('error')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['slug'] = slug
        return context


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')



class DeleteServiceView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Service
    context_object_name = 'services'
    success_url = reverse_lazy('freelance_homepage')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'account.can_delete_freelancer_page'

    def get_queryset(self):
        return super().get_queryset().filter(freelance=self.request.user)


    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('error')
        return redirect('loginFreelance')
