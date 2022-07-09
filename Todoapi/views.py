from django.shortcuts import render
from rest_framework.views import APIView
from Todoapi.models import Todos
from rest_framework.response import Response
from Todoapi.serializers import TodoSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework import authentication, permissions
from rest_framework import status, serializers

from rest_framework.viewsets import ViewSet, ModelViewSet

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

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
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = Todos.objects.filter(user=request.user)
        serializer = TodoSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data, context={"user": request.user})  # pass user as context
        # print(request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


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


#    Mixins

class TodosMixinView(GenericAPIView,
                     ListModelMixin,
                     CreateModelMixin):
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()

    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TodoMixinDetailsView(GenericAPIView,
                           RetrieveModelMixin,
                           UpdateModelMixin,
                           DestroyModelMixin):

    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TodoSerializer
    queryset = Todos.objects.all()
    lookup_url_kwarg = "todo_id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("not own user")

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# View Set

class TodosViewSetView(ViewSet):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = Todos.objects.filter(user=request.user)
        serializer = TodoSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data, context={"user": request.user})  # pass user as context
        # print(request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        todo = Todos.objects.get(id=id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print(kwargs)

        id = kwargs.get("pk")
        todo = Todos.objects.get(id=id)
        serializer = TodoSerializer(instance=todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        todo = Todos.objects.get(id=id)
        todo.delete()
        return Response({"msg": "deleted"})

# Model View Set


class TodosModelViewSetView(ModelViewSet):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = Todos
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data, context={"user": request.user})  # pass user as context
        # print(request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



