from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('profile/',views.profile,name="profile"),
    path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('upload/',views.upload,name="upload"),
    path('about/', views.about,name="about"),
    path('search/<str:key>', views.search,name="search"),
    path(r'delete?p_id=[\d]+/', views.delete_post,name="delete_post"),
    path('<str:business>',views.viewProfile,name="viewProfile"),
    path('<str:business>/products/<str:name>',views.viewPost,name="viewPost"),
    path('reset_password/',views.reset_password,name="reset_password"),
]