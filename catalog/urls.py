from django.urls import path

from catalog import views
from catalog.views import ProductModeratorUpdateView

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
    path(
        "products/<int:pk>/moderate/",
        ProductModeratorUpdateView.as_view(),
        name="product_moderator_update",
    ),
    path(
        "category/<int:category_id>/",
        views.CategoryProductListView.as_view(),
        name="category_products",
    ),
]
