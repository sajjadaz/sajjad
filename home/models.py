from django.db import models
from django.contrib.auth.models import User  # وارد کردن مدل کاربر
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.sender.username

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
