from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает базу данных и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        # 1. Сначала удаляем старые данные
        self.stdout.write("Очистка базы данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Загружаем данные из наших фикстур
        self.stdout.write("Загрузка данных из фикстур...")
        call_command("loaddata", "category_data.json")
        call_command("loaddata", "product_data.json")

        self.stdout.write(self.style.SUCCESS("База данных успешно перезаполнена!"))
