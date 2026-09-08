from django.shortcuts import render
from App_panel.models.Modules import Modules

def header(request):
    return render(request, "admin_layouts/header.html")

def footer(request):
    return render(request, "admin_layouts/footer.html")

def sidebar(request):
    modules = Modules.objects.all()
    if '/module/' in request.path:
        return render(request, "admin_layouts/sidebar_module.html", {'modules': modules})
    else:
        return render(request, "admin_layouts/sidebar.html")