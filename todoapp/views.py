from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import Task,Category
from .forms import TaskForm,CategoryForm,SignUpForms
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


class CategoryPage(View):
    def get(self,request,*args,**kwargs):
        try:
            context = {
                'category':Category.objects.filter(author=request.user),
                'form':CategoryForm(),
            }
            return render(request,'todoapp/category_page.html',context)
        except TypeError:
            return redirect('todoapp:login')

category_page = CategoryPage.as_view()

class CategoryCreate(View):
    def post(self,request,*args,**kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = result.user
            result.save()
            return redirect('todoapp:category_page')

category_create = CategoryCreate.as_view()

class CategoryUpdate(View):
    def post(self,request,*args,**kwargs):
        obj = Category.objects.get(pk=kwargs['category_pk'])
        form = CategoryForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('todoapp:category_page')

category_update = CategoryUpdate.as_view()

class CategoryDelete(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        category.delete()
        return redirect('todoapp:category_page')

category_delete = CategoryDelete.as_view()

class TaskLists(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        context = {
            'categorys':Category.objects.filter(author=request.user),
            'tasks':Task.objects.filter(category=category,author=request.user).order_by('conditions','-created_at'),
            'category_pk':kwargs['category_pk'],
        }
        return render(request,'todoapp/task_lists.html',context)

task_lists = TaskLists.as_view()

class TaskDetail(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        context = {
            'task':get_object_or_404(Task,pk=kwargs['task_pk'],category=category,author=request.user),
            'categorys':Category.objects.filter(author=request.user),
            'category_pk':kwargs['category_pk'],
        }
        return render(request,'todoapp/task_detail.html',context)

task_detail = TaskDetail.as_view()

class TaskCreate(View):
    def get(self,request,*args,**kwargs):
        context = {
            'categorys':Category.objects.filter(author=request.user),
            'form':TaskForm(),
            'category_pk':kwargs['category_pk'],
        }
        return render(request,'todoapp/task_create.html',context)

    def post(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        form = TaskForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = request.user
            result.category = category
            result.save()
            return redirect('todoapp:task_lists',category_pk=kwargs['category_pk'])

task_create = TaskCreate.as_view()

class TaskUpdate(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        task = get_object_or_404(Task,pk=kwargs['task_pk'],category=category,author=request.user)
        context = {
            'form':TaskForm(instance=task),
            'categorys':Category.objects.filter(author=request.user),
            'category_pk':kwargs['category_pk'],
        }
        return render(request,'todoapp/task_update.html',context)

    def post(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        task = get_object_or_404(Task,pk=kwargs['task_pk'],category=category,author=request.user)
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = request.user
            result.category = category
            result.save()
            return redirect('todoapp:task_lists',category_pk=kwargs['category_pk'])

task_update = TaskUpdate.as_view()


class TaskDelete(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        tasks = get_object_or_404(Task,pk=kwargs['task_pk'],category=category,author=request.user)
        tasks.delete()
        return redirect('todoapp:task_lists',category_pk=kwargs['category_pk'])

task_delete = TaskDelete.as_view()

class ConditionsChange(View):
    def get(self,request,*args,**kwargs):
        category = get_object_or_404(Category,pk=kwargs['category_pk'],author=request.user)
        tasks = get_object_or_404(Task,pk=kwargs['task_pk'],category=category)
        tasks.conditions = conditions_check(tasks.conditions)
        tasks.save()
        return redirect('todoapp:task_lists',category_pk=kwargs['category_pk'])

conditions_change = ConditionsChange.as_view()

def conditions_check(now_condition):
    if now_condition == 1:
        now_condition = 3
    elif now_condition == 2:
        now_condition = 3
    elif now_condition == 3:
        now_condition = 2
    return now_condition

class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'

    def form_valid(self,form):
        messages.success(self.request,"ログインしました")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.warning(self.request,"ログインできませんでした")
        return super().form_invalid(form)

class LogoutView(AuthLogoutView):
    template_name = 'accounts/logout.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = '/'

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        self.object = user
        messages.success(self.request,"追加しました")
        return redirect(self.get_success_url())

    def form_invalid(self,form):
        messages.warning(self.request,"追加できませんでした")
        return super().form_invalid(form)
