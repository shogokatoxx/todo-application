# from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from .models import Task

class Lists(ListView):
    model = Task

    def get_queryset(set):
        return Task.objects.order_by('-conditions','created_at')

class Detail(DetailView):
    model = Task

class Create(CreateView):
    model = Task
    fields = ('title','content','conditions')
    success_url = '/'

    def form_invalid(self,form):
        message.warning(self.request,"保存できませんでした")
        return super().form_invalid(form)

class Update(UpdateView):
    model = Task
    fields = ('title','content','conditions')
    success_url = '/'

    def form_invalid(self,form):
        message.warning(self.request,"保存できませんでした")
        return super().form_invalid(form)

class Delete(DeleteView):
    model = Task
    success_url = '/'
