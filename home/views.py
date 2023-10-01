from django.views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect

from product.models import Category
from .forms import MessageForm


class Home(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(self.request.session.get('myname', 'sajjad'))
        return context


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.instance.sender = request.user  # اختصاص مقدار ارسال‌کننده
            form.save()
            return redirect('main')  # یا به هر صفحه دیگری که می‌خواهید منتقل شوید
    else:
        form = MessageForm()
    return render(request, 'contactUs.html', {'form': form})


