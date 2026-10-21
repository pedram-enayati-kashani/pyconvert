from django.core.mail import EmailMessage, get_connection
from App_panel.models.EmailModel import EmailSettings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from Admin_panel.helpers.client.helper_client import get_site_info_value
from email.utils import formataddr

class EmailService:
    def __init__(self):
        lang = get_language()
        available_langs = [code for code, name in settings.LANGUAGES]
        if lang in available_langs:
            self.config = EmailSettings.objects.filter(status='active',lang=lang).first()
        else:
            self.config = EmailSettings.objects.filter(status='active', lang='fa').first()
        if not self.config:
            raise ValueError(_("Active email settings not found."))

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

def send_Email_Contact(contact, full_link):
    title = get_site_info_value("title")
    email_service = EmailService()
    subject = _("Reply to your message on %(title)s") % {'title': title}

    html_content = render_to_string('admin_panel/emails/contact_reply.html', {
        'contact': contact,
        'link': full_link,
    })
    text_content = strip_tags(html_content)

    email_service.send(
        subject=subject,
        body=text_content,
        to_emails=[contact.email],
        html_message=html_content
    )
    return True


def send_Email_test_connect(to_email):
    try:
        title = get_site_info_value("title")
        email_service = EmailService()
        subject = _("%(title)s - Email connection test") % {'title': title}

        html_content = render_to_string('admin_panel/emails/test_connection.html')
        text_content = strip_tags(html_content)

        email_service.send(
            subject=subject,
            body=text_content,
            to_emails=[to_email],
            html_message=html_content
        )
        return True, _("Message sent successfully.")

    except Exception as e:
        error_msg = _("Message failed to send. Error: %(error)s") % {'error': str(e)}
        return False, error_msg



