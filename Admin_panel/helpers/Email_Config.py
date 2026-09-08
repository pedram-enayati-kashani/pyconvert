from django.core.mail import EmailMessage, get_connection
from App_panel.models.EmailModel import EmailSettings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from Admin_panel.helpers.client.helper_client import get_site_info_value
from email.utils import formataddr

class EmailService:
    def __init__(self):
        self.config = EmailSettings.objects.filter(status='active').first()
        if not self.config:
            raise ValueError("تنظیمات ایمیل فعال پیدا نشد.")

    def get_connection(self):
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=self.config.host,
            port=self.config.port,
            username=self.config.username,
            password=self.config.password,
            use_tls=self.config.use_tls,
            use_ssl=self.config.use_ssl,
            timeout=30,
        )

    def send(self, subject, body, to_emails, html_message=None):
        connection = self.get_connection()

        from_name = self.config.sender_name or get_site_info_value("title")
        from_email = formataddr((from_name, self.config.sender_email))

        email = EmailMessage(
            subject=subject,
            body=html_message if html_message else body,
            from_email=from_email,
            to=to_emails if isinstance(to_emails, list) else [to_emails],
            connection=connection,
        )

        if html_message:
            email.content_subtype = 'html'

        return email.send(fail_silently=False)

def send_Email_Contact(contact,full_link):
    title = get_site_info_value("title")
    email_service = EmailService()
    subject = f"پاسخ به پیام شما در {title}"
    html_content = render_to_string('admin_panel/emails/contact_reply.html', {
        'contact': contact,
        'link': full_link,
    })
    text_content = strip_tags(html_content)
    email_service.send(subject=subject, body=text_content, to_emails=[contact.email], html_message=html_content)
    return True

def send_Email_test_connect(to_email):
    try:
        title = get_site_info_value("title") or "سیستم"
        email_service = EmailService()
        subject = f"{title} - تست اتصال ایمیل"
        html_content = render_to_string('admin_panel/emails/test_connection.html')
        text_content = strip_tags(html_content)

        email_service.send(
            subject=subject,
            body=text_content,
            to_emails=[to_email],
            html_message=html_content
        )

        return True, "پیام با موفقیت ارسال شد."
    except Exception as e:
        return False, f"پیام با مشکل روبرو شد. خطا: {str(e)}"



