from django.shortcuts import render
from rest_framework.views import APIView
from Todoapi.models import Todos
from rest_framework.response import Response
from Todoapi.serializers import TodoSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status


# Create your views here.

class UserCreationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=uname, password=password)
            if user:
                login(request, user)
                return Response({"msg": "success"})
            else:
                return Response({"msg": "invalid credentials"})




class TodosView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Todos.objects.all()
        serializer = TodoSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class TodoDetailView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("todo_id")
        todo = Todos.objects.get(id=id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("todo_id")
        todo = Todos.objects.get(id=id)
        serializer = TodoSerializer(instance=todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("todo_id")
        todo = Todos.objects.get(id=id)
        todo.delete()
        return Response({"msg":"deleted"})
