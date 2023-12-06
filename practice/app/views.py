from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import *
from .models import *


# Create your views here.

def index(request):
    app_last = Aplication.objects.order_by('-date').filter(status='done')[:4]
    app_haired = Aplication.objects.filter(status='haired').count()
    return render(request, 'app/index.html', context={'app_last': app_last, 'app_haired': app_haired})


class Login(LoginView):
    template_name = 'app/registration/login.html'


class CreateApplication(CreateView):
    form_class = AddAplForm
    template_name = 'app/aplication_add.html'
    success_url = '/profile/all'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def profile(request, status):
    if status == 'all':
        my_app_list = Aplication.objects.filter(user=request.user.pk).order_by('-date')
    else:
        my_app_list = Aplication.objects.filter(status=status).order_by('-date')
    return render(request, 'app/profile.html', context={'my_app_list': my_app_list})


def app_filter(request, status):
    app_list = Aplication.objects.filter(status=status).order_by('-date')
    return render(request, 'app/profile.html', context={'app_list': app_list, 'status': status})


def registration(request):
    if request.method == 'POST':
        form = Reg_Form(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.confirm_password = 'NULL'
            new_user = form.save()
            login(request, new_user)
            return render(request, 'app/profile.html')
    else:
        form = Reg_Form()

    return render(request, 'app/registration/registration.html', {'form': form})


def delete_request(request, request_id):
    request_obj = Aplication.objects.get(id=request_id)
    if request.method == 'POST':
        request_obj.delete()
        return redirect(reverse('profile', kwargs={'status': 'all'}))
    else:
        request_obj.delete()
        return redirect(reverse('app_list'))


def admin_app(request):
    if (request.method == 'POST'):
        form = AppListFormFilter(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status != 'all':
                queryset = Aplication.objects.filter(status=status).order_by('-date')
            else:
                form = AppListFormFilter()
                queryset = Aplication.objects.order_by('-date')
    else:
        form = AppListFormFilter()
        queryset = Aplication.objects.order_by('-date')

    return render(request, 'app/app_list.html', context={'form': form, 'queryset': queryset})


class AppAdminHandle(UpdateView):
    model = Aplication
    form_class = AppListHandleForm
    success_url = '/app_list/'
    template_name = 'app/app_handle.html'

    def get_object(self):
        post_id = self.kwargs.get('id')
        obj = get_object_or_404(Aplication, id=post_id)
        return obj


def category_view(request):
    cat_list = Category.objects.all()
    if request.method == 'POST':
        form = CategoryList(request.POST)
        if form.is_valid():
            Category.objects.create(**form.cleaned_data)
    else:
        form = CategoryList()
    return render(request, 'app/cat_list.html', context={'form': form, 'cat_list': cat_list})


def delete_category(request, id):
    request_obj = Category.objects.get(id=id)
    if request.method == 'POST':
        request_obj.delete()
        return redirect(reverse('category'))
