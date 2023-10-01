from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'created_at', 'subject')
    list_filter = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not change:  # اگر پیام جدیدی ایجاد می‌شود
            obj.sender = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Message, MessageAdmin)
