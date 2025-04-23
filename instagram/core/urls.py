from django.urls import path

from .views import RegisterView, LoginView,MyPostView,User_Post,Delete_or_edit_myPost

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('manage_my_post/',MyPostView.as_view()),
    path('get_user_post/<str:username>',User_Post.as_view()),
    path('edit_delete_my_post/<int:pk>',Delete_or_edit_myPost.as_view())
]