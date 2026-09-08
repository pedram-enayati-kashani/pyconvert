import json
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import UpdateView, CreateView, FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.apps import apps
from django.utils import timezone
from django.db import transaction, connection
from django.db.models import NOT_PROVIDED
from django.contrib.auth.models import Group
from django.contrib import messages
from App_panel.models import Page,Section
from App_panel.helpers.backup import SQLGenerator
from App_panel.forms.PageTable import TablePageForm
from App_panel.forms.SectionTable import TableSectionForm, SectionForm
from App_panel.forms.GroupTable import TableGroupForm
from App_panel.forms.TableQuery import SQLImportForm
from App_panel.models.Modules import Modules
from Admin_panel.helpers.pager import get_visible_page_numbers

class Index(ListView):
    template_name = 'App_panel/Tables/index.html'
    model = Page
    context_object_name = 'pages'

    def get_queryset(self):
        return Page.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['groups'] = Group.objects.all()
        context['modules'] = Modules.objects.all()

        return context

class PageCreate(FormView):
    template_name = 'App_panel/Tables/create.html'
    form_class = TablePageForm
    success_url = reverse_lazy('App_panel:table')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "ایجاد صفحات"
        return context

class SectionCreate(View):
    def get(self, request, *args, **kwargs):

        data = [
            {
                "title": "pyconvert",
                "name": "بخش معرفی بالای صفحه اصلی",
                "type": "no_post",
                "slug": "top-image",
            },
        ]
        for item in data:
            Section.objects.get_or_create(
                title= item["title"],
                name= item["name"],
                type= item["type"],
                slug= item["slug"],
            )
        return redirect(reverse_lazy('App_panel:table'))

class SectionIndex(ListView):
    template_name = 'App_panel/Tables/sections/index.html'
    paginate_by = 15
    model = Section
    context_object_name = 'sections'

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'paginator' in context and 'page_obj' in context:
             context['visible_page_numbers'] = get_visible_page_numbers(
                 paginator=context['paginator'],
                 page_obj=context['page_obj']
             )
        return context

class SectionUpdate(UpdateView):
    template_name = 'App_panel/Tables/sections/edit.html'
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy('App_panel:table-section')

class GroupCreate(View):
    def get(self, request, *args, **kwargs):
        data = [
            {"name":"admin","status":"active"},
            {"name":"author","status":"active"},
        ]
        for item in data:
            Group.objects.get_or_create(name= item["name"])
        return redirect(reverse_lazy('App_panel:table'))

class ModuleCreate(View):
    def get(self, request, *args, **kwargs):
        data = [
            {'title':"فرم ساز","name":"form_builder"},
            {'title':"منو ساز","name":"Menu_Builder"},
            {'title':"شبکه های اجتماعی","name":"social_media"},
            {'title':"تبلیغات متنی","name":"adv_text"},
            {'title':"تبلیغات بنر","name":"adv_image"},
            {'title':"هدایتگر آدرس‌ها","name":"redirect_rule"},
            {'title':"واترمارک","name":"watermark"},
            {'title':"املاک","name":"Real_Estate"},
            {'title':"رسانه","name":"media"},
        ]
        for item in data:
            Modules.objects.get_or_create(
                title=item["title"],
                name= item["name"]
            )
        return redirect(reverse_lazy('App_panel:table'))

class BaseExportView(View):
    db_type = "sqlite"

    def get(self, request, *args, **kwargs):
        generator = SQLGenerator(self.db_type)
        sql_output = []

        for model in apps.get_models():
            sql_output.append(generator.generate_for_model_with_m2m(model))

        response = HttpResponse(
            "\n".join(sql_output),
            content_type="application/sql"
        )
        filename = f"backup_{self.db_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sql"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

class ExportMySQLView(BaseExportView): db_type = "mysql"
class ExportPostgresView(BaseExportView): db_type = "postgres"

class InputPostgresSqlListView(TemplateView):
    template_name = "App_panel/Tables/input/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        models_data = []
        for model in apps.get_models():
            fields = []
            for field in model._meta.fields:
                if field.auto_created and not field.concrete:
                    continue
                fields.append({
                    "name": field.name,
                    "type": field.get_internal_type(),
                })

            models_data.append({
                "app_label": model._meta.app_label,
                "model_name": model._meta.model_name,
                "verbose_name": model._meta.verbose_name,
                "db_table": model._meta.db_table,
                "fields": fields,
            })

        context["models_data"] = models_data
        return context


class InputPostgresSqlDetailView(View):
    template_name = "App_panel/Tables/input/input.html"

    def get_model(self, app_label, model_name):
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            raise Http404("Model not found")

    def is_required_field(self, field):
        if field.auto_created and not field.concrete:
            return False

        if field.primary_key:
            return False

        if getattr(field, "auto_now", False) or getattr(field, "auto_now_add", False):
            return False

        if field.has_default():
            return False

        if field.null:
            return False

        if field.blank:
            return False

        if field.default is not NOT_PROVIDED:
            return False

        return True

    def get_fields(self, model):
        fields = []
        for field in model._meta.fields:
            if field.auto_created and not field.concrete:
                continue

            fields.append({
                "name": field.name,
                "type": field.get_internal_type(),
                "null": field.null,
                "blank": field.blank,
                "required": self.is_required_field(field),
                "primary_key": field.primary_key,
                "default": field.default if field.default is not NOT_PROVIDED else None,
            })
        return fields

    def get_context(self, model, **kwargs):
        return {
            "verbose_name": model._meta.verbose_name,
            "db_table": model._meta.db_table,
            "model_name": model._meta.model_name,
            "fields": self.get_fields(model),
            **kwargs
        }

    def get(self, request, app_label, model_name):
        model = self.get_model(app_label, model_name)
        return render(request, self.template_name, self.get_context(model))

    def post(self, request, app_label, model_name):
        model = self.get_model(app_label, model_name)
        raw_data = request.POST.get("raw_data", "").strip()

        try:
            data_list = json.loads(raw_data)

            if not isinstance(data_list, list):
                messages.error(request, "ورودی باید یک لیست JSON باشد.")
                return render(request, self.template_name, self.get_context(model))

            allowed_field_names = {
                f.name for f in model._meta.fields
                if not (f.auto_created and not f.concrete) and not f.primary_key
            }

            required_fields = {
                f.name for f in model._meta.fields
                if self.is_required_field(f)
            }

            objs = []
            for index, row in enumerate(data_list, start=1):
                if not isinstance(row, dict):
                    messages.error(request, f"رکورد شماره {index} باید یک آبجکت JSON باشد.")
                    return render(request, self.template_name, self.get_context(model))

                cleaned_row = {
                    key: value
                    for key, value in row.items()
                    if key in allowed_field_names
                }

                missing_fields = {
                    field_name for field_name in required_fields
                    if field_name not in cleaned_row or cleaned_row[field_name] in [None, ""]
                }

                if missing_fields:
                    messages.error(
                        request,
                        f"در رکورد شماره {index} فیلدهای اجباری وارد نشده‌اند: {', '.join(sorted(missing_fields))}"
                    )
                    return render(request, self.template_name, self.get_context(model))

                objs.append(model(**cleaned_row))

            if not objs:
                messages.error(request, "رکورد معتبری برای ذخیره پیدا نشد.")
                return render(request, self.template_name, self.get_context(model))

            with transaction.atomic():
                model.objects.bulk_create(objs)

            messages.success(request, f"{len(objs)} رکورد با موفقیت ذخیره شد.")
            return render(request, self.template_name, self.get_context(model))

        except json.JSONDecodeError:
            messages.error(request, "JSON ورودی معتبر نیست.")
            return render(request, self.template_name, self.get_context(model))
        except Exception as e:
            messages.error(request, f"خطا: {str(e)}")
            return render(request, self.template_name, self.get_context(model))


class InputPostgresQueryView(FormView):
    template_name = 'App_panel/Tables/input/query.html'
    form_class = SQLImportForm
    success_url = reverse_lazy('App_panel:table-input-query')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        sql_content = form.cleaned_data['sql_queries']
        queries = [q.strip() for q in sql_content.split(';') if q.strip()]

        executed_count = 0
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    for query in queries:
                        cursor.execute(query)
                        executed_count += 1

            messages.success(self.request, f"تعداد {executed_count} کوئری با موفقیت در دیتابیس اجرا شد.")
        except Exception as e:
            messages.error(self.request, f"خطا در اجرای کوئری‌ها: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)