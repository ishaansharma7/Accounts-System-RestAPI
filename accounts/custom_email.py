from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings

def activation_email(user_name, domain, pk, token, email):
    email_subject = 'Active your Account'
    message = render_to_string('emails/activation.html',
                            {
                                'user': user_name,
                                'domain': domain,
                                'uid': urlsafe_base64_encode(force_bytes(pk)),
                                'token': token
                            }
                            )

    email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_message.send(fail_silently=False)
    print('done')