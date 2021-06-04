from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>", views.entry, name="entry"),
    path("new", views.new_entry, name="new_entry"),
    path("edit/<str:page_name>", views.edit_entry, name="edit_entry"),
    path("random", views.random_page, name="random_page")
]
