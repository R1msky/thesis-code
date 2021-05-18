from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
import json

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from module.forms import AddRepoData, UserRegistrationForm
from module.models import User

session = requests.Session()


def index(request):
    return render(request, 'module/index.html')


def analyzer(request):
    return render(request, 'module/analyzer.html')


def dc_login(request):
    if request.user.is_authenticated:
        if session.get('https://www.deepcode.ai/publicapi/session') != 200:
            token, loginURL = session.post('https://www.deepcode.ai/publicapi/login').json().values()
            session.headers.update({'Session-Token': token, 'Content-Type': 'application/json'})
            return redirect(loginURL)
    else:
        return redirect('login')


def get_results(request, data):
    result = ''
    bundle = session.post(url='https://www.deepcode.ai/publicapi/bundle', data=json.dumps(data))
    if bundle.status_code == 200:
        bundleId = bundle.json().get('bundleId')
        resp = session.get(url='https://www.deepcode.ai/publicapi/analysis/{}'.format(bundleId))
        result = res_process(resp.json())
    elif bundle.status_code == 403:
        result = 'Ошибка 403. Указанный репозиторий не является публчиным или такого репозитория не существует,' \
                 ' либо неверно указан владелец.'
    elif bundle.status_code == 400:
        result = 'Ошибка 400. Введены некорректные данные.'
    elif bundle.status_code == 401:
        result = 'Ошибка 401. Отсутствует сессионный токен. Создайте новую сессию и войдите в Gitlab.'
    elif bundle.status_code == 413:
        result = 'Ошибка 413. Слишком большой объем переданных данных. Убедитесь, что ваш коммит не превышает 4 МБ.'
    return result


def show_results(request, result):
    return render(request, 'module/results.html', {'result': result})


def submit_process(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRepoData(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                result = get_results(request, data)
                if request.path == '/analyzer/results/':
                    return render(request, 'module/results.html', {'result': result})
        else:
            form = AddRepoData()
            return render(request, 'module/analyzer.html', {'form': form})
    else:
        return redirect('login')


def res_process(result):
    severities = {2: 0, 3: 0}
    msg = ''
    suggs = result.get('analysisResults').get('suggestions').values()
    for sugg in suggs:
        sev = sugg.get('severity')
        severities.update({sev: severities.get(sev) + 1})

    if severities.get(2) < 3:
        msg = 'В вашем коде {} предупреждения и {} критических ошибок. Ваш балл 4n'.format(severities.get(2),
                                                                                           severities.get(3))

    return msg


class RegisterUserView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'module/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse_lazy('home')
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title='Авторизация')
    #     return dict(list(context.items()) + list(c_def.items()))


class LogoutUserView(LoginRequiredMixin, LogoutView):
    next_page = 'login'


@login_required
def profile(request):
    return render(request, 'user/profile.html')

