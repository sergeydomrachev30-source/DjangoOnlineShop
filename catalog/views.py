from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Contacts, Product
from catalog.services import get_all_products, get_products_by_category


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products_list"
    paginate_by = 2

    def get_queryset(self):
        return get_all_products()


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


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "catalog/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "catalog/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get("pk"))
        if product.owner != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("Вы не являетесь владельцем этого продукта.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Достаем товар из базы по его первичному ключу (pk) и проверяем,
        является ли текущий пользователь владельцем"""
        product = get_object_or_404(Product, pk=kwargs.get("pk"))
        if product.owner != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("Вы не являетесь владельцем этого продукта.")
        return super().post(request, *args, **kwargs)


class ProductModeratorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = "catalog/create_product.html"
    form_class = ProductModeratorForm
    permission_required = "catalog.can_unpublish_product"
    success_url = reverse_lazy("home")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/confirm_delete_product.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get("pk"))
        if product.owner != request.user and not request.user.has_perm(
            "catalog.delete_product"
        ):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get("pk"))
        if product.owner != request.user and not request.user.has_perm(
            "catalog.delete_product"
        ):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
        return super().post(request, *args, **kwargs)


class CategoryProductListView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products_list"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return get_products_by_category(category_id)
