from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from .models import News


@receiver(post_save, sender=News)
def send_news_update_email(instance, created, **kwargs):
    print('Сигнал запущен!')
    if created:
        users = User.objects.filter(email__isnull=False)
        messages = []
        for user in users:
            message_subject = 'Новости нашего сайта'
            message_body = f'Уважаемый {user.username}, появилась новая новость: {instance.title}!'
            messages.append((message_subject, message_body, 'from@example.com', [user.email]))

        send_mass_mail(messages, fail_silently=False)
