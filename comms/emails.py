from django.core.mail import send_mail
from accounts.models import TempData
from django.template.loader import render_to_string


def send_conf_email(temp_email, email_conf):
    from_email = 'mikesdjangosite@gmail.com'
    to_email = temp_email
    subject = 'Accountabillibuddy Email Address Change'
    context = {
        'email_conf': email_conf
    }
    msg_plain = render_to_string('conf_email.txt', context)
    msg_html = render_to_string('conf_email.html', context)
    send_mail(
            subject,
            msg_plain,
            from_email,
            [to_email],
            html_message=msg_html
    )
    print('email sent')