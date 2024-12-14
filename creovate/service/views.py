from lib2to3.fixes.fix_input import context

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseForbidden
from django.contrib import messages


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView

from creovate.service.forms import AddServiceForm, UpdateServiceForm
from creovate.service.models import Service


# Create your views here.
class DetailServiceView(LoginRequiredMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'service/service_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category = self.object.category
        context['filtered_services'] = Service.objects.filter(category=current_category).exclude(id=self.object.id)
        return context


class AddServiceView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = AddServiceForm
    success_url = reverse_lazy('freelance_homepage')
    template_name = 'service/add_service.html'

    def form_valid(self, form):
        service = form.save(commit=False)
        service.freelance = self.request.user
        service.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class UpdateServiceView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = UpdateServiceForm
    context_object_name = 'service'
    success_url = reverse_lazy('freelance_homepage')
    template_name = 'service/update_service.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.freelance != request.user:
            messages.error(request, "You don't have permission to edit the service")
            return redirect('freelance_homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['slug'] = slug
        return context



class DeleteServiceView(LoginRequiredMixin, DeleteView):
    model = Service
    context_object_name = 'service'
    success_url = reverse_lazy('freelance_homepage')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(freelance=self.request.user)
