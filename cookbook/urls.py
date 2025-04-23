from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginuser, name="login"),
    path("logout", views.logoutuser, name="logout"),
    path("register", views.registeruser, name="register"),
    path("recipe/<int:card_id>/", views.recipe, name="recipe"),
    path("category/<int:categories_id>/", views.category, name="category"),  
    path("saved/<int:user_id>/", views.saved, name="saved"),
    path("top", views.top, name="top"),
    path("vote/<int:card_id>/", views.vote, name="vote"),
    path("savedrecipe/<int:card_id>/", views.savedrecipe, name="savedrecipe"), 
    path("search", views.search, name="search"),
    path("talk", views.talk, name="talk") 
]