from django.urls import path

from creovate.service.views import DetailServiceView, AddServiceView, UpdateServiceView, DeleteServiceView

urlpatterns = [
    path('<slug:slug>/', DetailServiceView.as_view(), name='service'),
    path('add_service/<str:username>/', AddServiceView.as_view(), name='add_service'),
    path('update_service/<slug:slug>/', UpdateServiceView.as_view(), name='update_service'),
    path('delete_service/<slug:slug>/', DeleteServiceView.as_view(), name='delete_service'),
]