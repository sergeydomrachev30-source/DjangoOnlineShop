from django import forms

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        """Валидация поля name (название товара)"""
        cleaned_data = self.cleaned_data["name"]
        name_lower = cleaned_data.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f"В названии товара нельзя использовать слово: '{word}'"
                )
        return cleaned_data

    def clean_description(self):
        """Валидация поля description (описание товара)"""
        cleaned_data = self.cleaned_data["description"]
        description_lower = cleaned_data.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(
                    f"В описании товара нельзя использовать слово: '{word}'"
                )
        return cleaned_data

    def clean_price(self):
        """Валидация поля price (название товара)"""
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

    def clean_image(self):
        """Валидацию для поля загрузки изображения"""
        image = self.cleaned_data.get("image")

        if not image:
            return image

        if image.size > 5242880:
            raise forms.ValidationError("Размер файла не должен превышать 5 МБ")

        image_lower = image.name.lower()
        if not image_lower.endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError("Разрешены только форматы JPEG (jpg) и PNG.")

        return image
