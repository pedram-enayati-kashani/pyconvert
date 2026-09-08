from django.shortcuts import render
from Admin_panel.helpers.client.helper_client import Get_menu_builder_links, Get_social_media, get_site_info_value
from Admin_panel.helpers.client.adv import get_adv_banners, get_adv_text_with_section

def header(request):
    return render(request, "layouts/header.html")

def footer(request):
    return render(request, "layouts/footer.html")

def menu(request,menu_name):
    if menu_name == "header":
        print(Get_menu_builder_links(menu_name))
        return render(request, "layouts/menu_header.html",Get_menu_builder_links(menu_name))
    elif menu_name == "footer":
        return render(request, "layouts/menu_footer.html",Get_menu_builder_links(menu_name))

def search_header(request):
    return render(request, "layouts/search_header.html")


def socialMedia(request):
    name = Get_social_media()
    return render(request, "layouts/socialMedia.html", {"social_media": name})

def faveicon(request):
    return render(request, "layouts/faveicon.html")

def adv_banner(request,section):
    return render(request,"component/adv/banner.html",{"banners":get_adv_banners(section)})

def adv_text(request,section):
    return render(request,"component/adv/text.html",get_adv_text_with_section(section))

def head_mata(request):
    return render(request, "layouts/head_tags.html",{"scripts":get_site_info_value("headMeta")} )

def footer_script(request):
    return render(request, "layouts/footer_scripts.html", {"scripts":get_site_info_value("footerScript")})