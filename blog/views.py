from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from blog.models import Blog
from django.urls import reverse_lazy
import os
from django.conf import settings


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "image", "is_published"]
    success_url = reverse_lazy("blog:list")


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            # Получаем путь к папке из settings.py (или используем по умолчанию)
            log_dir = getattr(settings, "EMAIL_FILE_PATH", "tmp/app-messages")
            os.makedirs(log_dir, exist_ok=True)

            # Создаем обычный текстовый файл на чистом русском языке
            file_path = os.path.join(log_dir, f"notification_article_{obj.pk}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Кому: my-email@yandex.ru\n")
                f.write("Тема: Поздравляем с достижением! \n\n")
                f.write(
                    f'Ваша статья "{obj.title}" набрала '
                    f'ровно 100 просмотров! Вы супер!\n'
                )

        return obj


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "image", "is_published"]

    def get_success_url(self):
        return reverse_lazy("blog:detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
