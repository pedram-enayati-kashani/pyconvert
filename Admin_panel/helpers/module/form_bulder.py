from App_panel.models.PostModel import Post
from module.models.FormBuilder import FieldValue, PostFormAssignment, FormField
from django.core.cache import cache
from django.utils import timezone

def get_post_form_fields_and_values(post_id):
    try:
        cache_key = f"post_form_fields_{post_id}"
        results = cache.get(cache_key)

        if results is not None:
            return results

        results = []

        # ۱. پیدا کردن فرم فعال منتسب به پست
        assignment = (
            PostFormAssignment.objects
            .filter(post_id=post_id)
            .select_related('form')
            .first()
        )

        if assignment and assignment.form and assignment.form.status == 'active':
            assigned_form = assignment.form

            # ۲. دریافت تمام فیلدهای فعال این فرم به ترتیب مشخص‌شده
            fields = (
                FormField.objects
                .filter(form_id=assigned_form.id, status='active')
                .order_by('order', 'id')
            )

            # ۳. دریافت تمام مقادیر ذخیره‌شده برای این پست و این فرم
            field_values_qs = (
                FieldValue.objects
                .filter(
                    post_id=post_id,
                    field__form_id=assigned_form.id,
                    field__status='active',
                )
            )
            # ساخت یک دیکشنری برای دسترسی سریع O(1) به مقادیر بر اساس field_id
            values_map = {fv.field_id: fv for fv in field_values_qs}

            # ۴. ترکیب فیلدها با مقادیر (یا مقدار خالی در صورت عدم وجود)
            for field in fields:
                saved_value = values_map.get(field.id)

                value = saved_value.value if saved_value else ""
                updated_at = str(saved_value.updated_at) if saved_value else str(timezone.now())

                results.append({
                    'post_id': post_id,
                    'field_id': field.id,
                    'field_label': field.label,
                    'field_name': field.name,
                    'field_type': field.field_type,
                    'prefix': field.prefix,
                    'suffix': field.suffix,
                    'order': field.order,
                    'value': value,
                    'updated_at': updated_at,
                })

        cache.set(cache_key, results, 600)
        return results

    except Exception as error:
        print(f'An error occurred while getting post custom fields: {error}')
        return []

