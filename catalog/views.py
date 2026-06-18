from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Contacts, Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products_list"
    paginate_by = 2


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
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "catalog/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "catalog/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/confirm_delete_product.html"
    success_url = reverse_lazy("home")
