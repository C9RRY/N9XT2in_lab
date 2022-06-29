from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from repair_shop.forms import *
from repair_shop.models import ClientCard
from django.contrib.auth.mixins import LoginRequiredMixin


menu = [
    {'title': "Черга", 'url_name': "queued"},
    {'title': "Прийомка", 'url_name': "new_order"},
]


def index(request):
    return render(request, 'repair_shop/index.html', {'title': 'Main', 'menu': menu})


def about(request):
    return render(request, 'repair_shop/about.html', {'title': 'Contacts', 'menu': menu})


# with class based view
# LoginRequiredMixin used for protect against not auth user
class Queued(LoginRequiredMixin, ListView):
    paginate_by = 12
    model = ClientCard
    template_name = 'repair_shop/queued.html'
    context_object_name = 'client_cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Черга'
        return context

    def get_queryset(self):
        return ClientCard.objects.filter(master=1)


class AddOrder(LoginRequiredMixin, CreateView):
    form_class = AddOrderForm
    template_name = 'repair_shop/new_order.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Прийомка'
        return context


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientCard
    template_name = 'repair_shop/card_update.html'
    fields = ['master', 'name', 'breakage']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Картка клієнта'
        return context


class WarrantyUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientCard
    template_name = 'repair_shop/card_update.html'
    fields = ['master', 'name', 'breakage', 'break_fix', 'price', 'warranty', 'is_fixed']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Картка клієнта'
        return context


class ShowCard(DetailView):
    model = ClientCard
    template_name = 'repair_shop/self_card.html'
    slug_url_kwarg = 'client_card_slug'
    context_object_name = 'client_card'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Картка клієнта'
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'repair_shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Реестрація'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'repair_shop/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Авторизація'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return render(request, 'repair_shop/index.html', {'title': 'Main', 'menu': menu})


class AdminWorkCabinet(ListView):
    paginate_by = 10
    model = ClientCard
    template_name = 'repair_shop/cabinet.html'
    context_object_name = 'client_cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Кабінет майстра'
        return context

    def get_queryset(self):
        return ClientCard.objects.filter(master=self.request.user, is_fixed=False)