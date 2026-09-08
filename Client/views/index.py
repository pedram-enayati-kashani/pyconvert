from django.shortcuts import render
from django.views.generic import ListView
from App_panel.models.PostModel import Post
from Admin_panel.helpers.client.search import get_result_query
from Admin_panel.helpers.client.helper_client import get_site_info_value
from Admin_panel.helpers.client.schema import homePageSchema
from Admin_panel.helpers.client.Page import getPostPage


def index(request):
    data = getPostPage("home", 10)
    schema = homePageSchema(request,data)
    context = {
        "title": get_site_info_value("title"),
        "title_seo": get_site_info_value("title_seo"),
        "description": get_site_info_value("description_seo"),
        "logo": get_site_info_value("logo"),
        "page": data["page"],
        "posts": data["posts"],
        "schema": schema,
    }

    return render(request, "pages/index.html", context)

class SearchView(ListView):
    model = Post
    template_name = "pages/search.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('s', '').strip()
        return get_result_query(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_title'] = self.request.GET.get('s', '')
        return context

def RobotsTXT(request):
    data = get_site_info_value('robotsText')
    return render(request,"pages/robots.txt",{'data':data},content_type="text/plain")


def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)