from catalog.models import Product, Contacts
from django.shortcuts import render


def home(request):
    last_five = Product.objects.all().order_by("-created_at")[:5]
    print("--- Последние 5 товаров на главной ---")
    for product in last_five:
        print(f"Товар: {product.name}, Цена: {product.price}")

    return render(request, "catalog/home.html")


def contacts(request):
    # Получаем заполненные контакты из базы данных (самую первую запись)
    contact_info = Contacts.objects.first()
    if request.method == "POST":
        name = request.POST.get("username")
        message = request.POST.get("message")

        # Для проверки вывод в терминал PyCharm
        print(f"Новое сообщение от {name}: {message}")

        # Передаем в шаблон флаг успеха и имя пользователя
        context = {"success": True, "user_name": name}
        return render(request, "catalog/contacts.html", context)

    # Передаем контакты в обычный шаблон при открытии страницы
    context = {"contact_info": contact_info}
    return render(request, "catalog/contacts.html", context=context)
