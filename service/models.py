from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class ClientOfService(models.Model):
    email = models.EmailField(
        max_length=100,
        verbose_name="ваша почта",
        help_text="введите вашу почту",
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name="ВАШЕ ФИО",
        help_text="введите ваше ФИО"
    )
    comments = models.TextField(
        max_length=200,
        verbose_name="ваш комментарий",
        help_text='оставьте свой комментарий',
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name}-{self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class MailingSettings(models.Model):

    PERIOD_DAILY = "daily"
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"

    PERIODS = (
        (PERIOD_DAILY, "Ежедневная"),
        (PERIOD_WEEKLY, "Раз в неделю"),
        (PERIOD_MONTHLY, "Раз в месяц"),
    )

    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_DONE = "done"

    STATUSES = (
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущен"),
        (STATUS_DONE, "Завершена"),
    )

    start_time = models.DateTimeField(verbose_name="время старта")
    end_time = models.DateTimeField(verbose_name="Время окончания", **NULLABLE)
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name="Период")
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name="Статус")
    message = models.ForeignKey("MailingMessage", on_delete=models.CASCADE, verbose_name="Сообщение", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ManyToManyField(ClientOfService, related_name="mailing_settings")

    def __str__(self):
        return f"{self.start_time} / {self.period}"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class MailingMessage(models.Model):
    subject = models.CharField(max_length=250, verbose_name="Тема")
    message = models.TextField(verbose_name="Тело")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Пиьсма"


class MailingLog(models.Model):
    STATUS_OK = "ok"
    STATUS_FAILED = "failed"
    STATUSES = (
        (STATUS_OK, "Успешно"),
        (STATUS_FAILED, "Ошибка")
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name="Дата последней попытки")
    client = models.ForeignKey(ClientOfService, on_delete=models.SET_NULL, verbose_name="Клиент", null=True, blank=True)
    settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, verbose_name="настройка", null=True,
                                 blank=True)

    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_OK, verbose_name="Статус")
    server_response = models.CharField(verbose_name='статус', max_length=350, **NULLABLE)

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"
