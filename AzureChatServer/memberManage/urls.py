from django.urls import path

from memberManage import views

urlpatterns = [
    path("login/", views.login),
    path('logout/', views.logout),
    path("signup/", views.signup),
    path("test/", views.test)
]
