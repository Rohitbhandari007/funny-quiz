from django.shortcuts import render, HttpResponse
from .models import *


def index(request):

    return render(request, 'core/index.html')


def room(request, room_name):

    quiz = Quiz.objects.filter(id=1)
    questions = Question.objects.filter(quiz__in=quiz)
    answers = Answer.objects.filter(question__in=questions)
    context = {
        'room_name': room_name,
        'quiz':quiz,
        'questions':questions,
        'answers':answers
    }

    return render(request, 'core/room.html', context)
