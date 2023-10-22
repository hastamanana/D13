from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Ad


@receiver(post_save, sender=Ad)
def notify_user_ad(sender, instance, created, **kwargs):
    if created:
        subject = (f'Новое объявление: {instance.title} '
                   f'{instance.posted.strftime("%d.%m.%Y")}')
        message = 'Появилось новое объявление!'
        user_emails = [user.email for user in User.objects.all()]
        html_content = render_to_string(
            'users/email/email_form.html',
            {
                'ad': instance,
                'message': message,
                'url': 'http://' +
                       Site.objects.get_current().domain +
                       instance.get_absolute_url()
            }
        )
        send_mail(
            subject=subject,
            message='',
            html_message=html_content,
            from_email=None,
            recipient_list=[user_emails]
        )
