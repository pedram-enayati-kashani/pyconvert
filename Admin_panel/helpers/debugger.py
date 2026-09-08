import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


def to_json_serializable(obj):
    """
    این تابع سعی می‌کند انواع مختلف اشیاء را به فرمتی قابل سریالایز شدن به JSON تبدیل کند.
    """
    if isinstance(obj, dict):
        # اگر دیکشنری بود، مقادیر آن را هم تلاش می‌کنیم قابل سریالایز کنیم
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # اگر لیست بود، عناصر آن را هم تلاش می‌کنیم قابل سریالایز کنیم
        return [to_json_serializable(elem) for elem in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))):
        # انواع داده‌ای که مستقیماً قابل سریالایز هستند
        return obj
    elif hasattr(obj, '__dict__'):
        # اگر شیء متد __dict__ داشت (مثلاً کلاس‌های پایتون سفارشی)
        # سعی می‌کنیم مقادیر attribute ها را به دیکشنری تبدیل کنیم
        return {k: to_json_serializable(v) for k, v in obj.__dict__.items()}
    elif hasattr(obj, 'all') and callable(obj.all):
        # اگر شیء یک QuerySet از Django بود، آن را به لیست تبدیل می‌کنیم
        return [to_json_serializable(item) for item in obj.all()]
    elif hasattr(obj, '__str__') and callable(obj.__str__):
        # اگر شیء متد __str__ داشت، آن را به رشته تبدیل می‌کنیم
        return str(obj)
    elif isinstance(obj, DjangoJSONEncoder):
        return obj
    else:
        try:
            return str(obj)
        except Exception:
            return f"<unserializable object: {type(obj).__name__}>"


def showData(obj_to_serialize):
    """
    این تابع هر نوع شیء را دریافت کرده و تلاش می‌کند آن را به صورت JSON برگرداند.
    """
    try:
        # ابتدا شیء را به فرمتی قابل سریالایز شدن تبدیل می‌کنیم
        serializable_data = to_json_serializable(obj_to_serialize)

        # سپس آن را با JsonResponse برمی‌گردانیم
        # DjangoJSONEncoder به طور خودکار تاریخ‌ها و برخی انواع دیگر را مدیریت می‌کند
        return JsonResponse(serializable_data, encoder=DjangoJSONEncoder, safe=False)

    except Exception as e:
        # اگر خطایی در تبدیل رخ داد، یک پیام خطا برمی‌گردانیم
        error_message = f"Failed to serialize object of type {type(obj_to_serialize).__name__}: {str(e)}"
        return JsonResponse({'error': error_message}, status=500)

