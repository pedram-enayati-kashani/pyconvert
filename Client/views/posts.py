from App_panel.models.PostModel import Post
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, F
from Client.forms.comment import CommentForm, SubCommentForm
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from App_panel.models.CommentsModel import Comments
from Admin_panel.helpers.module.form_bulder import get_post_form_fields_and_values
from Admin_panel.helpers.client.Post import get_post_details_with_relations, get_related_posts
from Admin_panel.helpers.client.most_visited import increase_post_views
from Admin_panel.helpers.client.schema import singlePostSchema

def posts(request):
    pass

def post_section(request):
    pass

class PostDetailView(DetailView):
    model = Post
    template_name = "pages/single.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "post_slug"
    form_class = CommentForm
    sub_form_class = SubCommentForm

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug:
            try:
                return get_post_details_with_relations(slug)
            except Post.DoesNotExist:
                raise Http404
            except Exception as e:
                print(f"Error in get_object for slug '{slug}': {e}")
                raise Http404
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        related_posts = get_related_posts(post.slug)
        context["schema"] = singlePostSchema(self.request, post,related_posts)
        context["related_posts"] = related_posts
        context["submission"] = get_post_form_fields_and_values(post)
        context["form"] = self.form_class()
        context["sub_form"] = self.sub_form_class()
        increase_post_views(self.request, post.id)
        return context

class SendCommentView(View):
    def post(self, request, post_slug, *args, **kwargs):
        post_obj = get_object_or_404(Post, slug=post_slug)
        parent_id = request.POST.get('parent_id')
        if parent_id:
            form = SubCommentForm(request.POST, post_obj=post_obj)
        else:
            form = CommentForm(request.POST, post_obj=post_obj)

        if form.is_valid():
            form.save()
            if parent_id:
                try:
                    parent_comment = Comments.objects.get(id=parent_id)
                    parent_comment.saw = 'not-see'
                    parent_comment.save()
                except Comments.DoesNotExist:
                    pass
            return JsonResponse({
                "success": True,
                "message": "دیدگاه شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود.",
            })

        errors_dict = {}
        for field, errors in form.errors.items():
            field_label = form.fields[field].label if field in form.fields else field
            errors_dict[field_label] = str(errors[0])

        return JsonResponse({
            "success": False,
            "message": "اطلاعات وارد شده معتبر نیست",
            "errors": errors_dict
        }, status=400)
