from django.core.mail import send_mail
from accounts.models import TempData
from django.template.loader import render_to_string
from buddy.keys import EMAIL_HOST_USER

def send_conf_email(temp_email, email_conf):
    from_email = EMAIL_HOST_USER
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
    
def send_warning_email(email, name):
    from_email = EMAIL_HOST_USER
    to_email = email
    subject = 'Accountabillibuddy: Event Warning'
    context = {
        'name': name
    }
    msg_plain = render_to_string('warning_email.txt', context)
    msg_html = render_to_string('warning_email.html', context)
    send_mail(
            subject,
            msg_plain,
            from_email,
            [to_email],
            html_message=msg_html
    )
    print('email sent')