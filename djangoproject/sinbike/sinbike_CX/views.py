from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

def main(request):
    """
    Display List
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'sinbike_CX/question_list.html', context)

def detail(request, question_id):
    """
    Display Question Content
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'sinbike_CX/question_detail.html', context)

def answer_create(request, question_id):
    """
    Answer
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('support:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'sinbike_CX/question_detail.html', context)

def question_create(request):
    """
    Create
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('support:main')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'sinbike_CX/question_form.html', context)