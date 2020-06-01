from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    name = request.GET.get('from-landing')
    counter_click.update({name: 1})
    print(counter_click)
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    name = request.GET.get('ab-test-arg')
    counter_show.update({name: 1})
    print(counter_show)
    if name == 'original':
        return render(request, 'landing.html')
    elif name == 'test':
        return render(request, 'landing_alternate.html')

    return render(request, landing)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': round((counter_click['test'] / counter_show['test']), 2),
        'original_conversion': round((counter_click['original'] / counter_show['original']), 2),
    })
