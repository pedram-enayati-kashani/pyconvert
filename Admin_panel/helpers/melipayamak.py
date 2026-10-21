from django.core.cache import cache
from melipayamak import Api
import random, requests
from django.conf import settings
from django.utils.translation import get_language
from App_panel.models.SMSModel import SMSSettings



# def send_otp_sms_pattern(phone_number, otp_code):
#     username = '9193030207'
#     password = '8d5cma'  # رمز عبور صحیح خود را جایگزین کنید
#     body_id = 506379
#
#     try:
#         api = Api(username, password)
#         # استفاده صریح از وب‌سرویس SOAP
#         sms = api.sms('soap')
#
#         # ترتیب آرگومان‌ها طبق مستندات مخزن رسمی: (text, to, bodyId)
#         response = sms.send_by_base_number(
#             str(otp_code),
#             str(phone_number),
#             body_id
#         )
#
#         print("MeliPayamak pattern response:", response, flush=True)
#
#         # بررسی ساختار پاسخ
#         if response:
#             try:
#                 # تبدیل پاسخ به عدد جهت اعتبارسنجی
#                 result_val = int(str(response).strip())
#                 # در وب‌سرویس ملی‌پیامک، شناسه‌های ثبت پیام (RecId) مقادیر بزرگی هستند.
#                 # کدهای خطای وب‌سرویس همگی مقادیر کوچک (معمولاً زیر 100 یا منفی) هستند.
#                 if result_val > 100:
#                     return {
#                         "success": True,
#                         "rec_id": result_val,
#                         "response": response,
#                     }
#                 else:
#                     return {
#                         "success": False,
#                         "error_code": result_val,
#                         "message": f"خطا در ارسال پیامک. کد خطا: {result_val}",
#                         "response": response,
#                     }
#             except ValueError:
#                 # اگر پاسخ قابل تبدیل به عدد نبود (مثلا دیکشنری یا ساختار دیگر بود)
#                 if isinstance(response, dict):
#                     if response.get("RetStatus") == 1:
#                         return {
#                             "success": True,
#                             "response": response,
#                         }
#                     return {
#                         "success": False,
#                         "message": response.get("StrRetStatus", "خطای نامشخص"),
#                         "response": response,
#                     }
#
#         return {
#             "success": False,
#             "message": "پاسخ خالی از سرور دریافت شد.",
#             "response": response,
#         }
#
#     except Exception as exc:
#         print("MeliPayamak pattern error:", str(exc), flush=True)
#         return {
#             "success": False,
#             "message": str(exc),
#         }

def send_otp_sms_pattern(phone_number, otp_code):
    lang = get_language()
    target_lang = lang if lang in ['fa', 'en'] else 'fa'
    sms_config = SMSSettings.objects.filter(status='active', lang=target_lang).first()

    if not sms_config:
        return {
            "success": False,
            "response": "No active SMS configuration found for this language."
        }

    try:
        api = Api(sms_config.username, sms_config.password)
        sms = api.sms('soap')
        response = sms.send_by_base_number(str(otp_code), str(phone_number), sms_config.body_id)
        result_val = int(str(response).strip())
        is_success = result_val > 0

    except Exception as e:
        return {
            "success": False,
            "response": str(e)
        }

    return {
        "success": is_success,
        "response": response
    }
