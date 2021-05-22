from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

def main(request):
    """
    Display List
    """
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    # Paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
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