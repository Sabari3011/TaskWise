from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("login/",views.getemail),
    path("otp/<str:email>/<int:valid>",views.sendotp),
    path("",views.home),
    path("logout/",views.logoutUser),
    path("delete/<int:id>",views.deletetask),
    path("update/<int:id>",views.updatetask),
    path("complete/<int:id>",views.complete)
]
