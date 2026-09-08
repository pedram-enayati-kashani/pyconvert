from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.db import transaction
from django.db.models import Count, Prefetch
from Admin_panel.forms.Contact import ContactForm
from ..forms.Filter import FilterForm
from ..helpers.pager import get_visible_page_numbers
from Admin_panel.mixin.auth import AdminRequiredMixin
from App_panel.models.ContactUsModel import ContactUs, ContactMessage
from Admin_panel.helpers.Email_Config import send_Email_Contact
from django.urls import reverse_lazy, reverse

class Index(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/contact/index.html'
    paginate_by = 15
    model = ContactUs
    context_object_name = 'contacts'
    form_class = FilterForm

    def get_queryset(self):
        return ContactUs.objects.annotate(
            messages_count=Count('messages')
        ).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class()
        if 'paginator' in context and 'page_obj' in context:
            context['visible_page_numbers'] = get_visible_page_numbers(
                paginator=context['paginator'],
                page_obj=context['page_obj']
            )
        return context


class Show(AdminRequiredMixin, DetailView):
    model = ContactUs
    template_name = 'admin_panel/contact/show.html'
    context_object_name = 'contact'
    form_class = ContactForm

    def get_queryset(self):
        return ContactUs.objects.prefetch_related(
            Prefetch(
                'messages',
                queryset=ContactMessage.objects.order_by('created_at'),
                to_attr='ordered_messages'
            )
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.saw != 'see':
            obj.saw = 'see'
            obj.save(update_fields=['saw'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context


class Reply(AdminRequiredMixin, View):
    def post(self, request, pk):
        contact = get_object_or_404(ContactUs, pk=pk)
        form = ContactForm(request.POST, request.FILES, user=request.user, ticket=contact)
        if form.is_valid():
            email_sent = False
            try:
                with transaction.atomic():
                    reply_instance = form.save()
                    contact.status = 'answered'
                    contact.save(update_fields=['status'])

                messages.success(request, 'پاسخ با موفقیت در سیستم ثبت شد.')
                try:
                    if contact.email:
                        token = contact.token
                        full_link = self.request.build_absolute_uri(
                            reverse('Client:contact-token', kwargs={'token_id': token})
                        )
                        email_sent = send_Email_Contact(contact,full_link)
                except Exception as mail_error:
                    messages.warning(request, f'پاسخ ثبت شد، اما خطایی در ارسال ایمیل رخ داد: {str(mail_error)}')

                if email_sent:
                    messages.info(request, 'ایمیل اطلاع‌رسانی با موفقیت برای کاربر ارسال شد.')

            except Exception as e:
                messages.error(request, f'خطای دیتابیس: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

        return redirect('Admin_panel:contact-show', pk=pk)


class Active(AdminRequiredMixin,View):
    model = ContactUs
    success_url = reverse_lazy('Admin_panel:page')
    def get(self, request, pk, *args, **kwargs):
        page = get_object_or_404(self.model, pk=pk)
        page.toggle_status()
        if page.status == 'active':
            messages.success(
                request,
                f"برچسب '{page.title}' فعال شد.",
            )
        else:
            messages.warning(
                request,
                f"برچسب '{page.title}' غیرفعال شد.",
            )

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(self.success_url)

class Query(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/page/index.html'
    paginate_by = 15
    model = ContactUs
    context_object_name = 'pages'
    form_class = FilterForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        queryset = super().get_queryset()
        if self.form.is_valid():
            status_filter = self.form.cleaned_data.get('status', 'all')
            if status_filter == 'active':
                queryset = queryset.filter(status='active')
            elif status_filter == 'inactive':
                queryset = queryset.filter(status='inactive')

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form

        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context


class Delete(AdminRequiredMixin, DeleteView):
    model = ContactUs
    success_url = reverse_lazy('Admin_panel:tag')