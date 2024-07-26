from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.utils import get_user_carts


def login(request):
    """Обрабатывает форму авторизации пользователя.

    Если отправляемые данные формы в POST-запросе валидны и пользователь существует в БД, то авторизует пользователя,
        выводит сообщение об успешном входе в личный кабинет и переправляет его либо по адресу в параметре next, если он есть,
        либо на главную страницу.

    Иначе отправить пользователю пустую форму.

    Args:
        request: Запрос пользователя.

    Returns:
        HttpResponse: Ответ, отображающий шаблон users/login.html с формой авторизации или перенаправляющий на главную страницу
            после успешной авторизации.
    """
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next")
                if redirect_page and redirect_page != reverse("user:logout"):
                    return HttpResponseRedirect(request.POST.get("next"))
                return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserLoginForm()

    context = {"title": "Авторизация", "form": form}
    return render(request, "users/login.html", context)


def registration(request):
    """Обрабатывает форму регистрации пользователя с сохранением текущей сессии.

    Если отправляемые данные формы в POST-запросе валидны, то сохраняет данные нового пользователя, получается ключ его сессии,
        авторизует и перенаправляет на главную страницу, в которой будут в том числе отображены те товары, которые он добавил
        до входа в личный кабинет.

    Иначе будет отправлена пустая форма геристрации.

    Args:
        request: Запрос пользователя.

    Returns:
        HttpResponse: Ответ, отображающий шаблон users/registration.html с формой регистрации или перенаправляющий на главную
            страницу после успешной регистрации
    """

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            session_key = request.session.session_key
            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(
                request,
                f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт",
            )
            return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserRegistrationForm()

    context = {
        "registration": "Home - Регистрация",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    """Обрабатывает форму редактирования профиля авторизованного пользователя.

    Если отправляемые данные формы в POST-запросе валидны, то обновляет профиль пользователя, выводит сообщение об успешном
        обновлении и перенаправляет пользователя на страницу, указанную в параметре 'next', или на текущую страницу,
        если 'next' не задан.

    Иначе отправляет пользователю форму с заполненными данными из профиля.

    Args:
        request: Запрос пользователя.

    Returns:
        HttpResponse: Ответ, отображающий шаблон 'users/profile.html' с формой редактирования профиля или перенаправляющий
            на страницу 'next' после успешного обновления.
    """
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Ваши данные обновлены")
            return HttpResponseRedirect(reverse("user:profile"))

    else:
        form = ProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product").order_by("-id"),
        )
    )

    
    context = {
        "profile": "Home - Личный кабинет",
        "form": form,
        "orders": orders,
    }

    return render(request, "users/profile.html", context)


@login_required
def logout(request):
    """Выполняет выход пользователя из аккаунта.

    Удаляет данные авторизации пользователя из сессии и выводит сообщение об успешном выходе.
    Перенаправляет пользователя на главную страницу.

    Args:
        request: Запрос пользователя.

    Returns:
        HttpResponseRedirect: Перенаправление на главную страницу.
    """
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))


def users_cart(request):
    """Отображает шаблон 'users_cart.html' сервиса 'users'."""
    return render(request, "users/users_cart.html")
