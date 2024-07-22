from django.db import models


class Blog(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Запись",
        help_text="Введите новую запись",
    )

    description = models.TextField(
        max_length=100,
        verbose_name="Описание",
    )
    photo = models.ImageField(
        upload_to="product/photo",
        verbose_name="Фото",
        help_text="Загрузите новое фото",
    )

    created_date = models.DateTimeField(
        blank=True, verbose_name="Дата создания", help_text="Введите дату загрузки",
        auto_now_add=True

    )

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["name", "description"]

    def __str__(self):
        return f"{self.name}-{self.description}"
