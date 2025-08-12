
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from rest_framework import authentication, permissions
from yaml import serialize
from .serializer import *
from .models import Project
from aaa.models import CustomUser
from aaa.serializers import UserSerializer
from aaa.permissions import IsAdminOrOwnerOrReadOnly


# Create your views here.

class ProjectList (APIView) :
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get(self, request) :
        projects = Project.objects.all()
        serialized_project = ProjectSerializer(projects, many=True)
        return Response(serialized_project.data)


    def post(self, request):
        serialized_project = ProjectSerializer(data=request.data)
        if serialized_project.is_valid():
            serialized_project.save()
            return Response(serialized_project.data, status=status.HTTP_201_CREATED)
        return Response(serialized_project.errors, status=HTTP_400_BAD_REQUEST)


class ProjectDetail (APIView):
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            return Project.objects.get(pk= pk)
        except :
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk= pk)
        serialized_project = ProjectSerializer(project)
        return Response(serialized_project.data)


    def put(self, request, pk):
        project = self.get_object(pk)
        serialized_project = ProjectSerializer(project, data = request.data , partial=True)
        if serialized_project.is_valid():
            serialized_project.save()
            return Response(serialized_project.data)
        return Response(serialized_project.errors, status= status.HTTP_400_BAD_REQUEST)


    def delete (self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(f"{project.title} deleted successfully" , status=status.HTTP_204_NO_CONTENT)


class ProjectOfUser (APIView):
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    def get (self, request, user_id) :
        projects = Project.objects.filter(users__id=user_id)
        serialized_project = ProjectSerializer(projects, many=True)
        return Response(serialized_project.data)


class ADDUserToProject (APIView):
    permission_classes = [IsAuthenticated,IsAdminOrOwnerOrReadOnly]

    def post(self, request, proj_id):
        user = request.user
        role = user.role
        user_id_to_add = request.data.get("id")

        if role == "OW":
            try:
                project = Project.objects.get(id=proj_id)
            except Project.DoesNotExist:
                return Response("project not found!")

            try:
                user_to_add = CustomUser.objects.get(id=user_id_to_add)
            except CustomUser.DoesNotExist:
                return Response("user not found!")

            project.users.add(user_to_add)
            return Response(f"user {user_to_add.username} added to project {project.title} successfully")

        else:
            return Response("only owners can have access!")


class ViewUsersOfProject (APIView):
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    def get(self, request, proj_id):
        try:
            project = Project.objects.get(id=proj_id)
        except Project.DoesNotExist :
            return Response("project not found ")

        serialized_users = UserSerializer(project.users.all(), many=True)
        return Response(serialized_users.data)
