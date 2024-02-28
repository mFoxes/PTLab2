from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase

# Create your views here.
def index(request):
    """Главная страница сайта, где можно выбрать товар для покупки"""
    products = Product.objects.all() # получение объектов товаров из базы данных
    context = {'products': products} # помещаем объекты в context для рендеринга
    return render(request, 'shop/index.html', context) # рендеринг страницы и ответ на запрос


class PurchaseCreate(CreateView):
    """Страница оформления покупки товара"""
    model = Purchase # выбор класса для результата формы
    fields = ['product', 'person', 'address'] # поля, заполняемые формой

    def form_valid(self, form):
        """Вызывается при успешной отправке формы и
        фиксирует покупку пользователем товара"""

        purchase = form.save(commit=False) # сохранения результата формы в объект без записи в БД
        product = purchase.product # получение товара, который был куплен
        if product.amount == 0:
            # сообщение о том, что товара нет в наличии
            return HttpResponse("<h1>400 Bad Request</h1>"
                                "<br>Продукта нет в наличии!", status=400)
        product.amount -= 1
        product.save()
        purchase.save()
        return HttpResponse(f'Спасибо за покупку, {purchase.person}!<p><a href="/">Назад</a></p>')

