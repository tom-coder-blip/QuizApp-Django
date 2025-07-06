from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect 
from .models import Quiz, Question
from django.contrib.auth import login 
from django.shortcuts import render, redirect
from .forms import QuizForm
from .forms import QuestionForm
from django.contrib.admin.views.decorators import staff_member_required 

def quiz_list(request):
    quizzes = Quiz.objects.all()

    #If the request is from HTMX, return only a partial HTML response.
    if request.headers.get("HX-Request"):
        return render(request, 'quiz/partials/quiz_list_partial.html', {'quizzes': quizzes})
    
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Check if the request is from HTMX
    if request.headers.get("HX-Request"):
        return render(request, 'quiz/partials/quiz_detail_partial.html', {'quiz': quiz})
    
    # If it's a normal request, return the full page
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def register(request):   #come back to it
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return render(request, 'quiz/partials/quiz_item.html', {'quiz': quiz})  #Return only new quiz item
    else:
        form = QuizForm()

    if request.headers.get("HX-Request"):
        return render(request, 'quiz/partials/quiz_form.html', {'form': form})  # Return only form if HTMX
    
    return render(request, 'quiz/create_quiz.html', {'form': form})

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form, 'quiz': quiz})

@staff_member_required 
def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/update_quiz.html', {'form': form})

@staff_member_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz_detail', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'quiz/update_question.html', {'form': form})

@staff_member_required
def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('quiz_list')

@staff_member_required 
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz_id = question.quiz.id
    question.delete()
    return redirect('quiz_detail', quiz_id=quiz_id) 