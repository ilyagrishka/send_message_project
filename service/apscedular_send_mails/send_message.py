from datetime import datetime
import pytz
from django.utils import timezone
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from service.models import MailingSettings, MailingLog


def send_email(message_settings, message_client):
    try:
        send_mail(
            subject=message_settings.message.subject,
            message=message_settings.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.email],
            fail_silently=False,
        )

        MailingLog.objects.create(
            time=timezone.now(),
            status="Успешно",
            mailing_list=message_settings,
            client=message_client,
        )
    except smtplib.SMTPException as e:
        MailingLog.objects.create(
            time=timezone.now(),
            status="Ошибка",
            server_response=str(e),
            mailing_list=message_settings,
            client=message_client,
        )


def send_message():
    print("=" * 30)
    time_zone = pytz.timezone(settings.TIME_ZONE)
    datetime_now = datetime.now(time_zone)
    for mailing_setting in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        print("+" * 30)

        if (datetime_now > mailing_setting.start_time) and (datetime_now < mailing_setting.end_time):
            print("-" * 30)
            for mailing_client in mailing_setting.client.all():
                mailing_log = MailingLog.objects.filter(
                    client=mailing_client.pk,
                    mailing_list=mailing_setting
                )

                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-time').first().time

                    if mailing_setting.periodicity == MailingSettings.PERIOD_DAILY:
                        if (datetime_now - last_try_date).days >= 1:
                            send_email(mailing_setting, mailing_client)
                elif mailing_setting.periodicity == MailingSettings.PERIOD_WEEKLY:
                    if (datetime_now - last_try_date).days >= 7:
                        send_email(mailing_setting, mailing_client)
                    elif mailing_setting.periodicity == MailingSettings.PERIOD_MONTHLY:
                        if (datetime_now - last_try_date).days >= 30:
                            send_email(mailing_setting, mailing_client)
                else:
                    send_email(mailing_setting, mailing_client)

# получаем текущую дату с учётом тайм зоны
# получить рассылки с учётом текущей даты и статуса

# проверить периодичность
# получить сообщение для рассылки и клиентов для рассылки
# пройтись по клиентам и отправить рассылку
# создать запись попытки
