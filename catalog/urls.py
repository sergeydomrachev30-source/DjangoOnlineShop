from django.urls import path
from catalog.views import home, contacts, product_detail, create_product

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("products/create/", create_product, name="create_product"),
]
