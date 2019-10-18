from django.urls import path
from . import views

app_name = 'todoapp'

urlpatterns = [
    path('',views.Lists.as_view(),name='lists'),
    path('<int:pk>',views.Detail.as_view(),name="detail"),
    path('update/<int:pk>',views.Update.as_view(),name="update"),
    path('delete/<int:pk>',views.Delete.as_view(),name="delete"),
    path('create',views.Create.as_view(),name='create'),
]
