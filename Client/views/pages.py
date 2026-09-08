from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages import get_messages
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import Count, Prefetch
from django.views import View
from Admin_panel.helpers.client.Page import getPage
from App_panel.models.ContactUsModel import ContactUs
from Client.forms.contactUs import ContactUsModelForm
from Client.forms.Contact_Form_Show import ContactForm, ContactMessage
from Admin_panel.helpers.client.schema import page_schema
from Admin_panel.helpers.Email_Config import send_Email_Contact


class AboutView(DetailView):
    template_name = "pages/page.html"
    context_object_name = "page"

    def get_object(self):
        return getPage('about')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema"] = page_schema(self.request, self.object)
        return context

class contact(CreateView):
    template_name = 'pages/contact.html'
    form_class = ContactUsModelForm
    success_url = reverse_lazy('Client:contact')

    def form_valid(self, form):
        self.object = form.save()
        token_str = self.object.token
        full_link = self.request.build_absolute_uri(
            reverse('Client:contact-token', kwargs={'token_id': token_str})
        )

        try:
            send_Email_Contact(self.object, full_link)
        except Exception:
            pass

        messages.success(
            self.request,
            'پیام شما با موفقیت ثبت شد. لینک پیگیری و گفتگو به ایمیل شما ارسال گردید.',
            extra_tags='contact_success_msg'
        )

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            message_list = []
            for m in get_messages(self.request):
                message_list.append({
                    'tag': m.tags,
                    'message': m.message
                })

            return JsonResponse({
                'status': 'success',
                'messages': message_list,
            })

        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = getPage("contact")
        context["schema"] = page_schema(self.request, page)
        context['page'] = page
        return context

class ContactViewToken(DetailView):
    model = ContactUs
    template_name = 'pages/contact_show.html'
    context_object_name = 'contact'
    form_class = ContactForm
    slug_field = "token"
    slug_url_kwarg = "token_id"

    def get_queryset(self):
        return ContactUs.objects.prefetch_related(
            Prefetch(
                'messages',
                queryset=ContactMessage.objects.order_by('created_at'),
                to_attr='ordered_messages'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

class ContactTokenReply(View):
    def post(self, request, token_id):
        contact = get_object_or_404(ContactUs, token=token_id)
        form = ContactForm(request.POST, request.FILES, user=request.user, ticket=contact)

        if form.is_valid():
            form.save()
            contact.status = 'pending'
            contact.saw = 'not-see'
            contact.save(update_fields=['status', 'saw', 'updated_at'])
            messages.success(request, 'پاسخ با موفقیت در سیستم ثبت شد.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

        return redirect('Client:contact-token', token_id=token_id)

class PageView(DetailView):
    template_name = "pages/page.html"
    context_object_name = "page"

    def get_object(self):
        slug = self.kwargs["page_slug"]
        return getPage(slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema"] = page_schema(self.request, self.object)
        return context