from django.urls import path

from catalog import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path("products/create/", views.ProductCreateView.as_view(), name="create_product"),
    path(
        "products/<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="update_product",
    ),
    path(
        "products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="delete_product",
    ),
]
