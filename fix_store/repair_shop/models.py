import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from datetime import datetime


class ClientCard(models.Model):
    is_fixed = models.BooleanField(default=False, verbose_name='Відремонтовано')
    brand = models.CharField(max_length=50, verbose_name='Модель')
    package = models.CharField(max_length=250, verbose_name='Комплектація')
    breakage = models.CharField(max_length=250, verbose_name='Опис несправності')
    name = models.CharField(max_length=150, verbose_name='П.І.Б клієнта')
    phone_number = models.CharField(max_length=250, verbose_name='Номер телефона клієнта')
    in_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата прийому')
    master = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, max_length=200, unique=True)
    break_fix = models.CharField(null=True, max_length=250, verbose_name='Проведений ремонт')
    price = models.IntegerField(null=True, verbose_name='Ціна')
    warranty = models.CharField(default='3 міс.', null=True, max_length=50, verbose_name='Гарантія')
    out_date = models.DateTimeField(null=True, max_length=50, verbose_name='Дата видачі')

    def __str__(self):
        return f"{self.in_date} {self.name}"

    def get_absolute_url(self):
        return reverse('queued')


class FilesAdmin(models.Model):
    admin_upload = models.FileField(upload_to='media')
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = str(uuid.uuid1())
    instance.out_date = datetime.now()


def phone_correct(sender, instance, *args, **kwargs):
    print(instance.phone_number)
    instance.phone_number = instance.phone_number.replace(' ', '')


pre_save.connect(phone_correct, sender=ClientCard)
pre_save.connect(slug_generator, sender=ClientCard)
