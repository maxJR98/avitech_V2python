from celery import shared_task

@shared_task
def send_email(subject, recipient, body):

    print(f'Enviando email a {recipient}: {subject}')