from django import forms

from home.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['email', 'subject', 'message']  # فقط فیلد پیام نمایش داده می‌شود
