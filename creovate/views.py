from django.shortcuts import render


def landing(request):
    return render(request, template_name='common/landing.html')

def about(request):
    return render(request, template_name='common/about.html')

def services(request):
    return render(request, template_name="common/service.html")