from rest_framework import serializers
from .models import *


#Tag, Task, SubTask, Comment , Log

class TaskSerializer(serializers.ModelSerializer):
    # title = serializers.SerializerMethodField()
    class Meta :
        model = Task
        fields = "__all__"
    # def get_title(self,obj):
    #     return  "ggg"


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta :
        model = SubTask
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Log
        fields = "__all__"

    def get_user(self,obj):
        return obj.username