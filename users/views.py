from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.db.models.base import Model as Model
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from cache.users.mixins import UserOrdersCacheMixin
from django.core.cache import cache


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)

            if session_key:
                old_carts = Cart.objects.filter(user=user)

                if old_carts.exists():
                    old_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(CreateView):
    """Обрабатывает форму регистрации пользователя с сохранением текущей сессии."""
    
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт!")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UserOrdersCacheMixin, UpdateView):
    """Обрабатывает форму редактирования профиля авторизованного пользователя."""
    
    template_name = "users/profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user:profile")

    def form_valid(self, form):
        messages.success(self.request, "Ваши данные обновлены")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def orders_caching(self):
        """Запрашивает информацию о заказах пользователя, кэширует ее и возвращает полученные данные."""
        
        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        
        set_cache_orders = self.set_cache(
            orders, f"user_{self.request.user.id}_orders", 60
        )
        return set_cache_orders
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Личный кабинет"
        context["orders"] = self.orders_caching()
        return context


class UserCartView(TemplateView):
    """Отображает корзину со списком товаров текущего пользователя."""
    
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))