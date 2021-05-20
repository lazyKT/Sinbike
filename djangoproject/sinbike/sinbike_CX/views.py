from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

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
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'sinbike_CX/question_detail.html', context)