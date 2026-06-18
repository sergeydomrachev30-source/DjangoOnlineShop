from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from catalog.models import Product, Contacts
from django.shortcuts import render
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product  # Заменяет строчку: Product.objects.all()
    template_name = "catalog/home.html"  # Заменяет строчку: render(request, "catalog/home.html", context)
    context_object_name = (
        "products_list"  # Заменяет ключ в словаре context: "products_list"
    )
    paginate_by = 2  # Заменяет строчки с Paginator, page_number и page_obj


class ContactsView(View):
    def get(self, request):
        contact_info = Contacts.objects.first()
        context = {"contact_info": contact_info}
        return render(request, "catalog/contacts.html", context)

    def post(self, request):
        contact_info = Contacts.objects.first()
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
        return render(request, "catalog/contacts.html", context=context)


class ProductDetailView(DetailView):
    model = Product  # Из какой модели брать объект
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "catalog/create_product.html"
    fields = ["name", "description", "price", "category", "image"]
    success_url = reverse_lazy("home")
