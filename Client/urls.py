from django.urls import path
from django.views.generic import TemplateView
from Client.views.index import index, SearchView, RobotsTXT
from Client.views.pages import AboutView, contact, PageView, ContactViewToken, ContactTokenReply
from Client.views.posts import PostDetailView, SendCommentView
from Client.views.section import SectionView
from Client.views.tag import tags, TagView
from Client.views.category import CategoryView, categories

app_name = "Client"
urlpatterns = [
    path("",index,name="home"),
    path("search",SearchView.as_view(),name="search"),
    path("about",AboutView.as_view(),name="about"),
    path("contact",contact.as_view(),name="contact"),
    path("contact/token/<str:token_id>",ContactViewToken.as_view(),name="contact-token"),
    path("contact/token/<str:token_id>/reply",ContactTokenReply.as_view(),name="contact-token-reply"),
    path("about/tags",TagView.as_view(),name="tags"),
    path("p/<str:page_slug>",PageView.as_view() , name="page"),
    # path("sec",sections,name="section-all"),
    path("sec/<str:section_slug>",SectionView.as_view(),name="section"),
    # path("post",posts,name="post-all"),
    path("post/<str:post_slug>",PostDetailView.as_view(),name="post"),
    path("post/<str:post_slug>/comment",SendCommentView.as_view(),name="comment"),
    # path("tag",tags,name="tags"),
    path("tag/<str:tag_slug>",TagView.as_view(),name="tag"),
    path("category",categories,name="categories"),
    path("category/<str:cat_slug>",CategoryView.as_view(),name="category"),
    path("robots.txt",RobotsTXT,name="robots"),
]