from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from .models import Task
from .forms import TaskForm

class Lists(ListView):
    model = Task

    def get_queryset(set):
        return Task.objects.order_by('-conditions','created_at')

class Detail(DetailView):
    model = Task

class Create(CreateView):
    model = Task
    form_class = TaskForm
    success_url = '/'
    template_name = "todoapp/task_create.html"

    def form_valid(self,form):
        messages.success(self.request,"保存しました") #messages.infoでもメッセージは送れる
        return super().form_valid(form) #return redirect(reverse('todoapp:lists'))にすると「ログインしました」の文字だけ送られDBへは保存できてなかった
                                        #基本汎用ビューではもともとあるメソッドをうまく使う方がいい

    def form_invalid(self,form):
        messages.warning(self.request,"保存できませんでした")
        return super().form_invalid(form)

class Update(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/'
    template_name = "todoapp/task_update.html"

    def form_valid(self,form):
        messages.success(self.request,"保存しました")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.warning(self.request,"保存できませんでした")
        return super().form_invalid(form)

# class Delete(DeleteView):
#     model = Task
#     success_url = '/'

def delete(request,pk):
    tasks = get_object_or_404(Task,pk=pk)
    tasks.delete()
    return redirect('todoapp:lists')

def conditions_change(request,pk):
    tasks = get_object_or_404(Task,pk=pk)
    if tasks.conditions == 1:
        tasks.conditions = 3
    elif tasks.conditions == 2:
        tasks.conditions = 3
    elif tasks.conditions == 3:
        tasks.conditions = 1
    tasks.save()
    return redirect('todoapp:lists')
