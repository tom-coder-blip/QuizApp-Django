from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('register/', views.register, name='register'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('<int:quiz_id>/update/', views.update_quiz, name='update_quiz'),
    path('questions/<int:question_id>/update/', views.update_question, name='update_question'),
    path('quiz/<int:pk>/delete/', views.delete_quiz, name='delete_quiz'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
]