# component
from django.shortcuts import render

def header(request):
    return render(request, "App_layouts/header.html")

def footer(request):
    return render(request, "App_layouts/footer.html")

def sidebar(request):
    return render(request, "App_layouts/sidebar.html")