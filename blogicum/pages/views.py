from django.shortcuts import render


def about(request):
    """Функция отвечающая за описание проекта."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Функция отвечающая за правила на сайте."""
    template = 'pages/rules.html'
    return render(request, template)
