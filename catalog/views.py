from django.shortcuts import render

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        message = request.POST.get('message')

        # Для проверки вывод в терминал PyCharm
        print(f"Новое сообщение от {name}: {message}")

        # Передаем в шаблон флаг успеха и имя пользователя
        context = {
            'success': True,
            'user_name': name
        }
        return render(request, 'catalog/contacts.html', context)
    return render(request, 'catalog/contacts.html')
