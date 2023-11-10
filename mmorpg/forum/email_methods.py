from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post

def send_notification_about(post: Post, author: User, response_text: str):
    html_content = render_to_string(
        'post_email.html',
        {
            'author_response_name': author.username,
            'response_text': response_text,
            'link': f'{settings.SITE_URL}/forum/{post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'На вашу статью \'{post.heading}\' оставили отклик!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[post.user.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_notification_about_response(post: Post, author: User):
    html_content = render_to_string(
        'response_email.html',
        {
            'post_author_username': post.user.username,
            'link': f'{settings.SITE_URL}/forum/{post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Автор стстьи \'{post.heading}\' оценил ваш отклик!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()