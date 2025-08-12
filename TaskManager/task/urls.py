from django.contrib import admin
from django.urls import path, include, re_path

from .views import *

# path("api/tasks/", include("task.urls"))

urlpatterns = [
    path("task_list/", TaskList.as_view({'get':'list'})),
    path("task_list/<int:pk>/", TaskDetails.as_view()),
    path("toggle_completed/<int:task_id>/", ToggleCompleted.as_view()),
    path("task_of_user/<int:user_id>/", TaskOfUser.as_view()),

]
