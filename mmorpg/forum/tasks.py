from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Response


@shared_task
def weekly_mailing():
    types = Post.get_types()
    recipients = {}
    for type in types:
        emails = []
        type_key = type[0]
        responses = Response.objects.filter(post__types=type_key)
        for response in responses:
            email = response.user.email
            if not emails.__contains__(email):
                emails.append(email)
        recipients[type_key] = emails
    
    for recipient in recipients:

        print(recipients, recipients[recipient], recipient)

        type_name = ""
        for type in types:
            if type[0] == recipient:
                type_name = type[1]
        emails = recipients[recipient]

        html_content = render_to_string(
            'weekly_news.html',
            {
                'type_name': type_name,
                'link': f'{settings.SITE_URL}forum/',
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails,
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    print('Рассылка произведена!')
