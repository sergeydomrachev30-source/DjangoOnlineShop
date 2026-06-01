from django.core.paginator import Paginator

from catalog.models import Product, Contacts, Category
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    # Извлекаем все товары из базы,
    products = Product.objects.all()
    # Создаем пагинатор. Указываем, сколько товаров
    # выводить на одной странице (например, 2)

    paginator = Paginator(products, 2)
    # Получаем номер текущей страницы из URL-адреса
    page_number = request.GET.get("page")

    # Получаем список товаров конкретно для этой страницы
    page_obj = paginator.get_page(page_number)

    # Складываем их в словарь контекста
    context = {
        "products_list": page_obj,
    }

    # Передаем контекст в шаблон
    return render(request, "catalog/home.html", context)


def contacts(request):
    # Получаем заполненные контакты из базы данных (самую первую запись)
    contact_info = Contacts.objects.first()
    if request.method == "POST":
        name = request.POST.get("username")
        message = request.POST.get("message")

        if not name or not message:
            context = {
                "contact_info": contact_info,
                "error": "Пожалуйста, "
                         "заполните все обязательные поля!",  # Передаем ошибку
            }
            return render(request, "catalog/contacts.html", context)

        print(f"Новое сообщение от {name}: {message}")

        context = {"success": True, "user_name": name, "contact_info": contact_info}
        return render(request, "catalog/contacts.html", context)

    context = {"contact_info": contact_info}
    return render(request, "catalog/contacts.html", context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def create_product(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, pk=category_id)

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image,
        )

        return redirect("home")

    return render(request, "catalog/create_product.html", {"categories": categories})
