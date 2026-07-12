from django.core.cache import cache

from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает список продуктов для указанной категории из кэша,
    либо из БД, если кэш пуст."""
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)
    if products is None:
        products = list(Product.objects.filter(category_id=category_id))
        cache.set(cache_key, products, 60 * 15)
    return products


def get_all_products():
    """Возвращает QuerySet всех продуктов из кэша Redis
    с поддержкой пагинации."""
    cache_key = "all_products_queryset"
    products_queryset = cache.get(cache_key)

    if products_queryset is None:
        # Берем QuerySet из базы данных
        products_queryset = Product.objects.all()
        # Насильно заставляем Django загрузить данные внутрь этого QuerySet
        products_queryset._fetch_all()
        # Сохраняем наполненный QuerySet в Redis
        cache.set(cache_key, products_queryset, 60 * 15)

    return products_queryset
