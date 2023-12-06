from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.CharField(max_length=254, verbose_name='Почта', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)

    def full_name(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def __str__(self):
        self.full_name()


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', blank=False)

    def __str__(self):
        return self.name


def validate_image_size(img):
    filesize = img.file.size
    megabyte_max = 2.0
    if filesize > megabyte_max * 1024 * 1024:
        raise ValidationError("Максимальный размер %sMB" % str(megabyte_max))


class Aplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    name = models.CharField(max_length=250, verbose_name='Название', null=False, blank=False)
    description = models.CharField(max_length=250, verbose_name='Описание', null=False, blank=False)
    Category = models.ForeignKey(Category, verbose_name='Категория', blank=False, null=False,
                                 on_delete=models.CASCADE)
    photo_file = models.ImageField(verbose_name='Фото', upload_to='photo', blank=False,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                               validate_image_size])
    date = models.DateTimeField(verbose_name='Дата заявки', auto_now_add=True)
    status = models.CharField(max_length=250, verbose_name='Статус', choices=[
        ('new', 'Новая'),
        ('done', 'Выполнено'),
        ('haired', 'Принято в работу')
    ], default='new')
    comment = models.CharField(max_length=250, verbose_name='Комментарий', blank=True)
    photo_file2 = models.ImageField(verbose_name='Фото готовой заявки', upload_to='photo', blank=False,
                                    validators=[
                                        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                        validate_image_size])

    def __str__(self):
        return f"{self.name} | {self.Category} | {self.get_status_display()}"
