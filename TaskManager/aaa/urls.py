from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
   TokenObtainPairView
)
from .views import *

# path("api/users/", include("aaa.urls"))

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users_list/" , UserList.as_view()),
    path("users_list/<int:pk>/", UserDetail.as_view()),
    path("not_completed/<int:user_id>/", GetNOTCompletedTasks.as_view()),
    path("expired_deadline/<int:user_id>/", DeadlineExpired.as_view()),
    path("sort_startdate/<int:user_id>/", SortProjectByStartDate.as_view()),

]