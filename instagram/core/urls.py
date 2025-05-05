from django.urls import path

from .views import RegisterView, LoginView, MyPostView, User_Post, Delete_or_edit_myPost, CommentCreateView, \
    CommentListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('manage_my_post/',MyPostView.as_view()),
    path('get_user_post/<str:username>',User_Post.as_view()),
    path('edit_delete_my_post/<int:pk>',Delete_or_edit_myPost.as_view()),

    path('posts/createComment/', CommentCreateView.as_view()),
    path('posts/<int:post_id>/comments/list/', CommentListView.as_view())

]