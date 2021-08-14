from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    """
    Home
    """
    msg = 'My Message'
    return render(request, 'main.html',{'message':msg})

def main(request):
    """
    Support main
    """
    return render(request, 'sinbike_CX/support_main.html')

def list(request):
    """
    Display Question List
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

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    Answer
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('support:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_create(request):
    """
    Create Ticket
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('support:main')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'sinbike_CX/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    Edit Ticket
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'Not Authorized')
        return redirect('support:main', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('support:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'sinbike_CX/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    Delete Ticket
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'Not Authorized')
        return redirect('support:main', question_id=question.id)
    question.delete()
    return redirect('support:main')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    Edit Answer
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, 'Not Authorized')
        return redirect('support:main', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('support:main', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'sinbike_CX/answer_form.html', context)