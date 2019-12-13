from django.urls import path
from . import views

app_name = 'todoapp'

urlpatterns = [
    path('',views.category_page,name='category_page'),
    path('category_create',views.category_create,name='category_create'),
    path('<int:category_pk>/category_update',views.category_update,name='category_update'),
    path('<int:category_pk>/category_delete',views.category_delete,name='category_delete'),
    path('<int:category_pk>',views.task_lists,name='task_lists'),
    path('<int:category_pk>/task_detail/<int:task_pk>',views.task_detail,name='task_detail'),
    path('<int:category_pk>/task_create',views.task_create,name='task_create'),
    path('<int:category_pk>/task_update/<int:task_pk>',views.task_update,name='task_update'),
    path('<int:category_pk>/task_delete/<int:task_pk>',views.task_delete,name='task_delete'),
    path('<int:category_pk>/conditions_change/<int:task_pk>',views.conditions_change,name='conditions_change'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('signup',views.SignUpView.as_view(),name="signup"),
]
