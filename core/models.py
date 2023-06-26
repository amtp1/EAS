from enum import Enum
from os.path import splitext
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage

class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/{uuid4().hex + ext}"


class User(AbstractUser):
    my_phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Номер телефона')
    home_phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Домашний номер телефона')
    address = models.CharField(max_length=255, null=True, verbose_name='Адрес проживания')
    birthday_date = models.DateField(null=True, verbose_name='Дата рождения')
    profile_pic = models.ImageField(storage=UUIDFileStorage(), null=True, blank=True, verbose_name='Изображение')
    links = models.ForeignKey('Links', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Ссылки на соц. сети')
    graduate = models.ForeignKey('Graduate', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Выпускник')
    employer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Работодатель')

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Graduate(models.Model):
    class Education(Enum):
        without = ('without', 'Без образования')
        medium = ('medium', 'Среднее образование')
        sec_voc = ('secondary_vocational', 'Среднее профессиональное образование')
        higher = ('higher', 'Высшее образование')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    education = models.CharField(max_length=80, choices=[x.value for x in Education],
                                 default=Education.get_value('without'), verbose_name='Образование')
    work_experience = models.TextField(verbose_name='Навыки и опыт работы')

    def __str__(self):
        return f"Выпускник #{self.id}"

    class Meta:
        db_table = 'graduates'
        verbose_name = 'Выпускник'
        verbose_name_plural = 'Выпускники'


class Employer(models.Model):
    company_name = models.CharField(max_length=128, verbose_name='Название компании')
    work_area = models.CharField(max_length=255, verbose_name='Сфера деятельности')
    image = models.ImageField(storage=UUIDFileStorage(), null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'employers'
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'


class Vacancy(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, verbose_name='Работодатель')
    profession = models.CharField(max_length=255, null=True, verbose_name='Профессия')
    demands = models.TextField(verbose_name='Требования')
    description = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата и время создания')

    class Meta:
        db_table = 'vacancies'
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Resume(models.Model):
    graduate = models.ForeignKey(Graduate, on_delete=models.PROTECT, verbose_name='Выпускник')
    description = models.TextField(null=True, verbose_name='Описание')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата и время создания')

    class Meta:
        db_table = 'resume'
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


class Links(models.Model):
    telegram = models.URLField(null=True, verbose_name='Telegram')
    whats_app = models.URLField(null=True, verbose_name='WhatsApp')

    class Meta:
        db_table = 'links'
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
