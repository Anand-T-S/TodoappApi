from django.urls import path
from Todoapi import views


urlpatterns = [
    path("todos", views.TodosView.as_view()),
    path("todos/<int:todo_id>", views.TodoDetailView.as_view()),
    path("users/accounts/signup", views.UserCreationView.as_view()),
    path("users/accounts/signin", views.SigninView.as_view()),
    path("todosmixin", views.TodosMixinView.as_view()),
    path("todosmixin/details/<int:todo_id>", views.TodoMixinDetailsView.as_view()),

]