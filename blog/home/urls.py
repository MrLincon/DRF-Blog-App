from django.urls import path
from .views import AddBlogView, FetchBlogView, FetchBlogByIdView, SearchBlogView, UpdateBlogView, DeleteBlogView

urlpatterns = [
    path('add/', AddBlogView.as_view()),
    path('fetch-all/', FetchBlogView.as_view()),
    path('fetch-single/<str:uid>', FetchBlogByIdView.as_view()),
    path('search/<str:searched>', SearchBlogView.as_view()),
    path('update/<str:uid>', UpdateBlogView.as_view()),
    path('delete/<str:uid>', DeleteBlogView.as_view()),
]
