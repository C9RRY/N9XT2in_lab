from radio_st.tmux_with_radio import radio_run_sh
from django.shortcuts import render, redirect
from radio_st.forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# def radio_list(request):
#     radios = Radios.objects.all()
#     return render(request, 'radio_st/radio.html', {'radios': radios})


def radio_run(request):
    if request.GET:
        if request.GET.get('play') == "True":
            url = request.GET.get('url')
            radio_run_sh.play_st(f'{url}')
            return redirect('radio')
        elif request.GET.get('play') == "False":
            radio_run_sh.play_st('')
            return redirect('radio')
        return render(request, 'radio_st/radio_run.html')
    return render(request, 'radio_st/radio_run.html')


class RadioList(LoginRequiredMixin, ListView):
    paginate_by = 12
    model = Radios
    template_name = 'radio_st/radio.html'
    context_object_name = 'radios'
    queryset = Radios.objects.filter().order_by('id').reverse()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список станцій'
        return context


class AddStation(LoginRequiredMixin, CreateView):
    form_class = AddRadioSt
    template_name = 'radio_st/new_station.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прийомка'
        return context


class DeleteStation(LoginRequiredMixin, DeleteView):
    model = Radios
    template_name = 'radio_st/delete_st.html'
    success_url = '/radio'


class RadioEdit(LoginRequiredMixin, UpdateView):
    model = Radios
    template_name = 'radio_st/edit_st.html'
    fields = ['title', 'url']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit station'
        return context
