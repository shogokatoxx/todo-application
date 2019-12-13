from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from .models import Task,Category
from .forms import TaskForm,CategoryForm,SignUpForms
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def category_page(request):
    try:
        category = Category.objects.filter(author=request.user)
        form = CategoryForm()
        return render(request,'todoapp/category_page.html',{'category':category,'form':form})
    except TypeError:
        return redirect('todoapp:login')

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = request.user
            result.save()
            return redirect('todoapp:category_page')

def category_update(request,category_pk):
    if request.method == 'POST':
        obj = Category.objects.get(pk=category_pk)
        form = CategoryForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('todoapp:category_page')

def category_delete(request,category_pk):
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    category.delete()
    return redirect('todoapp:category_page')

def task_lists(request,category_pk):
    categorys = Category.objects.filter(author=request.user)
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    tasks = Task.objects.filter(category=category,author=request.user).order_by('conditions','-created_at')
    return render(request,'todoapp/task_lists.html',{'tasks':tasks,'category_pk':category_pk,'categorys':categorys})

def task_detail(request,category_pk,task_pk):
    categorys = Category.objects.filter(author=request.user)
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    task = get_object_or_404(Task,pk=task_pk,category=category,author=request.user)
    return render(request,'todoapp/task_detail.html',{'task':task,'category_pk':category_pk,'categorys':categorys})

def task_create(request,category_pk):
    categorys = Category.objects.filter(author=request.user)
    form = TaskForm()
    if request.method == 'POST':
        category = get_object_or_404(Category,pk=category_pk,author=request.user)
        form = TaskForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = request.user
            result.category = category
            result.save()
            return redirect('todoapp:task_lists',category_pk=category_pk)
    return render(request,'todoapp/task_create.html',{'form':form,'categorys':categorys,'category_pk':category_pk})

def task_update(request,category_pk,task_pk):
    categorys = Category.objects.filter(author=request.user)
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    task = get_object_or_404(Task,pk=task_pk,category=category,author=request.user)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            result = form.save(commit=False)
            result.author = request.user
            result.category = category
            result.save()
            return redirect('todoapp:task_lists',category_pk=category_pk)
    return render(request,'todoapp/task_update.html',{'form':form,'categorys':categorys,'category_pk':category_pk})

def task_delete(request,category_pk,task_pk):
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    tasks = get_object_or_404(Task,pk=task_pk,category=category,author=request.user)
    tasks.delete()
    return redirect('todoapp:task_lists',category_pk=category_pk)

def conditions_change(request,category_pk,task_pk):
    category = get_object_or_404(Category,pk=category_pk,author=request.user)
    tasks = get_object_or_404(Task,pk=task_pk,category=category)
    tasks.conditions = conditions_check(tasks.conditions)
    tasks.save()
    return redirect('todoapp:task_lists',category_pk=category_pk)

def conditions_check(x):
    if x == 1:
        x = 3
    elif x == 2:
        x = 3
    elif x == 3:
        x = 2
    return x

class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'

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
        return redirect(self.get_success_url())

# class Lists(ListView):
#     model = Task
#
#     def get_queryset(set):
#         return Task.objects.order_by('-conditions','created_at')

# class Detail(DetailView):
#     model = Task

# class Create(CreateView):
#     model = Task
#     form_class = TaskForm
#     success_url = '/'
#     template_name = "todoapp/task_create.html"
#
#     def form_valid(self,form):
#         messages.success(self.request,"保存しました") #messages.infoでもメッセージは送れる
#         return super().form_valid(form) #return redirect(reverse('todoapp:lists'))にすると「ログインしました」の文字だけ送られDBへは保存できてなかった
#                                         #基本汎用ビューではもともとあるメソッドをうまく使う方がいい
#
#     def form_invalid(self,form):
#         messages.warning(self.request,"保存できませんでした")
#         return super().form_invalid(form)
#
# class Update(UpdateView):
#     model = Task
#     form_class = TaskForm
#     success_url = '/'
#     template_name = "todoapp/task_update.html"
#
#     def form_valid(self,form):
#         messages.success(self.request,"保存しました")
#         return super().form_valid(form)
#
#     def form_invalid(self,form):
#         messages.warning(self.request,"保存できませんでした")
#         return super().form_invalid(form)
