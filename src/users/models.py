from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import os
import hashlib


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле email обязательно!")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Кастомная модель пользователя с email вместо username"""
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def set_custom_password(self, raw_password) -> None:
        """Кастомизация хеширования пароля"""
        salt = os.urandom(16) # создаём уникальную соль
        # хешируем пароль с солью
        hashed = hashlib.pbkdf2_hmac(
            'sha256',  # алгоритм
            raw_password.encode('utf-8'),  # пароль в байтах
            salt,  # соль
            100000  # количество итераций
        )
        # сохраняем соль и хеш в поле password в формате: salt$hash
        self.password = salt.hex() + '$' + hashed.hex()

    def check_custom_password(self, raw_password)  -> bool :
        """Проверка пароля по кастомному хешу"""
        try:
            salt_hex, hashed_hex = self.password.split('$')
            salt = bytes.fromhex(salt_hex)
            hashed_check = hashlib.pbkdf2_hmac(
                'sha256',
                raw_password.encode('utf-8'),
                salt,
                100000
            )
            return hashed_check.hex() == hashed_hex
        except Exception:
            return False

    def __str__(self):
        return self.email
