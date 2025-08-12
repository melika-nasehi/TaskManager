from . import views
from django.urls import path,include
from .views import *


urlpatterns = [

    path("project_list/" , ProjectList.as_view()),
    path("project_list/<int:pk>/", ProjectDetail.as_view()),
    path("project_of_user/<int:user_id>/", ProjectOfUser.as_view()),
    path("add_user/<int:proj_id>/", ADDUserToProject.as_view()),
    path("users_of_project/<int:proj_id>/", ViewUsersOfProject.as_view()),


]