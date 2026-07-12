from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        permission_unpublish = Permission.objects.get(codename="can_unpublish_product")
        permission_delete = Permission.objects.get(codename="delete_product")

        group.permissions.add(permission_unpublish, permission_delete)
        self.stdout.write(self.style.SUCCESS("Группа модератора успешно настроена!"))

        blog_group, _ = Group.objects.get_or_create(name="Контент-менеджер")

        blog_permissions = Permission.objects.filter(
            codename__in=[
                "add_blog",
                "change_blog",
                "delete_blog",
                "add_post",
                "change_post",
                "delete_post",
            ]
        )

        if blog_permissions.exists():
            blog_group.permissions.add(*blog_permissions)
            self.stdout.write(
                self.style.SUCCESS("Группа контент-менеджера успешно настроена!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Права для блога не найдены. Убедитесь, что "
                    "миграции приложения blog применены."
                )
            )
