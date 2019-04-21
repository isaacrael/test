from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
#from django.core.urlresolvers import reverse
from django.urls import reverse
from . models import Answer, Question
import random
import datetime
from django.utils.encoding import *
# The line below imports the user_response variable from the user_response.py file
from . user_response import user_response
#from processors import custom_processor
from django.db.models import Sum
from . models import Ftq_Question, Ftq_Answer
from . models import Mc_Question, Mc_Answer
import re


# Create your views here.


# renders the About page located at cdh_ecosystem_quiz/cdh_ecosystem_quiz/index.html

def index(request):
    return render(request, 'index.html')


def logout(request):
    return render(request, 'cdh_ecosystem_quiz/logout.html')


# cut & paste views.py from giturdone below here
#
#
# The following functions are for the Short Answer Quiz
# quiz_selection page takes a user_response as input and displays associated quiz on Sensei Quiz page

def quiz_selection(request):
    if request.method == 'POST':
        user_response = request.POST.get('textfield', None)
        user_response = smart_text(user_response)
        f = open('cdh_ecosystem_quiz/user_response.py', 'w')
        # the line below write the text 'user_response = ' and concats the user_response the str function gets rid of u in front of string
        f.write('user_response = ' + repr(str(user_response)))
        f.close()
    return render(request, 'cdh_ecosystem_quiz/quiz_selection.html')


# git_quiz displays the quiz selected by user in the Quiz Selection page

#def git_quiz(request):
def quiz(request):
    if request.method == 'POST':
        user_response = request.POST.get('textfield', None)
        user_response = smart_text(user_response)
#        f = open('cdh_ecosystem_quiz/user_response.py', 'w')
#        # the line below write the text 'user_response = ' and concats the user_response the str function gets rid of u in front of string
#        f.write(str(user_response))
#        f.close()
        f = open('cdh_ecosystem_quiz/user_response.py', 'w')
        # the line below write the text 'user_response = ' and concats the user_response the str function gets rid of u in front of string
        f.write('user_response = ' + repr(str(user_response)))
        f.close()
    else:
        f = open('cdh_ecosystem_quiz/user_response.py', 'rb')
        user_response = f.read()
        f.close()
        # regular expression below reads the text between single quotes
        user_response = re.findall(rb"'(.*?)'", user_response, re.DOTALL)
        # reads the first element in the user_response list
        user_response=user_response[0]
        user_response = smart_text(user_response)
    if user_response == '':
        return render(request, 'cdh_ecosystem_quiz/index.html')
    if user_response == '1':
        latest_question_list = Question.objects.filter(category="Apache NiFi")
    if user_response == '2':
        latest_question_list = Question.objects.filter(category="Git Undoing Changes")
    if user_response == '3':
        latest_question_list = Question.objects.filter(category="Git Rewriting History")
    if user_response == '4':
        latest_question_list = Question.objects.filter(category="Git Branches")
    if user_response == '5':
        latest_question_list = Question.objects.filter(category="Git Remote Repositories")
    if user_response == '6':
        latest_question_list = Question.objects.filter(category="Git Config")
    if user_response == '7':
        latest_question_list = Question.objects.filter(category="Git Log")
    if user_response == '8':
        latest_question_list = Question.objects.filter(category="Git Diff")
    if user_response == '9':
        latest_question_list = Question.objects.filter(category="Git Reset")
    if user_response == '10':
        latest_question_list = Question.objects.filter(category="Git Rebase")
    if user_response == '11':
        latest_question_list = Question.objects.filter(category="Git Pull")
    if user_response == '12':
        latest_question_list = Question.objects.filter(category="Git Push")
    context = {'user_response': user_response, 'latest_question_list': latest_question_list}
    return render(request, 'cdh_ecosystem_quiz/index.html', context)


def git_resources(request):
        return render(request, 'cdh_ecosystem_quiz/resources.html')

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'cdh_ecosystem_quiz/detail.html', {'question': question})


def results(request, question_id):
    latest_question_list = Question.objects.order_by('?')
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        selected_answer = Answer.objects.get(question_id=question.id)
        # Gets my_answer -> the answer associated with question_id
        my_answer = Answer.objects.filter(question_id=question_id)
        # Get the image "post_image/filename" for my_answer
        for item in my_answer:
            image = item.image
        image=str(item.image)

        # Concatenates "/media/" + "post_image/filename"
        image=("/media/" + (image))
        user_answer = request.POST.get('textfield', None)
        # Get the question object
        q = Question.objects.get(pk=question_id)
        # Get all the answers associated with the question object
        a = q.answer_set.all()
        # Get the first element in the list of answers
        value = a[0]
        # smart_text is a django utility that converts an object to a unicode string
        correct_answer = smart_text(value)
        # code for score calculator
        # initialize variables
        sum = 0
        total_correct_answers=0
        ttl_correct = 0
        ttl_c = 0
        total_wrong_answers = 0
        ttl_wrong = 0
        ttl_w = 0
        ttl_questions_answered = 0
        score = 0
        Grade = str("")
        # if correct answer increment total_correct_answers by 1 for the selected answer
        if correct_answer == user_answer:
            selected_answer.total_correct_answers += 1
            selected_answer.save()
        else:
        # if wrong answer increment total_wrong_answers by for the selected answer
            selected_answer.total_wrong_answers += 1
            selected_answer.save()
        # add up all the total_correct_answers -> produces a dictionary
        ttl_correct = Answer.objects.aggregate(Sum('total_correct_answers'))
        # assign the dictionary value to ttl_c
        ttl_c = (ttl_correct["total_correct_answers__sum"])
        # add up all the total_wrong_answers -> produces a dictionary
        ttl_wrong = Answer.objects.aggregate(Sum('total_wrong_answers'))
        # assign the dictionary value to ttl_w
        ttl_w = (ttl_wrong["total_wrong_answers__sum"])
        # calculate total questions answered
        ttl_questions_answered = ttl_c + ttl_w
        # calculate quiz score
        score = (float(ttl_c)/float(ttl_questions_answered) * 100)
        # make score and integer so that if elif statements below handle the score value correctly
        score = round(int(score), 2)
        if score in range(90,101):
            Grade = "A"
        elif score in range(80,90):
            Grade = "B"
        elif score in range(70,80):
            Grade = "C"
        elif score in range(60,70):
            Grade = "D"
        elif score in range(0,59):
            Grade = "F"
        context = {'latest_question_list': latest_question_list, 'answer': user_answer,
        'question': question, 'correct_answer': correct_answer, 'Grade':Grade,
        'score':score, 'total_questions_answered': ttl_questions_answered,
        'total_correct_answers': ttl_c, 'total_wrong_answers': ttl_w, 'image': image}
    return render(request, 'cdh_ecosystem_quiz/results.html', context)


def reset_scores(request):
    answer_item = 0
    answers = Answer.objects.all()
    for answer_item in answers:
        answer_item.total_correct_answers = 0
        answer_item.total_wrong_answers = 0
        answer_item.save()
    return render(request, 'cdh_ecosystem_quiz/reset_scores.html')

def short_answer_quiz_categories(request):
    if request.method == 'POST':
        return render(request, 'cdh_ecosystem_quiz/index.html')
    else:
        return render(request, 'cdh_ecosystem_quiz/short_answer_quiz_categories.html')

# The following function renders the Tools Page

def tools(request):
    return render(request, 'cdh_ecosystem_quiz/tools.html')


# The functions below are for the Feynman Technique Quiz


def feynman_technique_quiz(request):
    ftq_questions = Ftq_Question.objects.all()
    context = {'ftq_questions': ftq_questions}
    return render(request, 'cdh_ecosystem_quiz/feynman_technique_quiz.html', context)

def ftq_detail(request, question_id):
    question = get_object_or_404(Ftq_Question, pk=question_id)
    return render(request, 'cdh_ecosystem_quiz/ftq_detail.html', {'question': question})

def ftq_results(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Ftq_Question, pk=question_id)
        #question = Ftq_Question.objects.filter(question_id=pk)
        #question = "test"
        # Gets my_answer -> the answer associated with question_id
        correct_answer = Ftq_Answer.objects.filter(question_id=question.id)
        # Initial the "knowledge field values to 0"
        knowledge_mastery = 0
        knowledge_needs_improvement = 0
        knowledge_black_hole = 0
        for item in correct_answer:
            correct_answer = item.answer_text
            image = item.image
            knowledge_mastery = item.knowledge_mastery
            knowledge_needs_improvement = item.knowledge_needs_improvement
            knowledge_black_hole = item.knowledge_black_hole
        image = str(item.image)
        # Get the image "post_image/filename" for my_answer
        # Concatenates "/media/" + "post_image/filename"
        image = ("/media/" + (image))
        # context dictionary allows the key value pairs to be available to the ftq_results.html page
        context = {'question': question, 'correct_answer': correct_answer,
        'image': image, 'knowledge_mastery': knowledge_mastery,
        'knowledge_needs_improvement': knowledge_needs_improvement, 'knowledge_black_hole': knowledge_black_hole}
    return render(request, 'cdh_ecosystem_quiz/ftq_results.html', context)

def ftq_reset_scores(request):
    answer_item = 0
    answers = Ftq_Answer.objects.all()
    """    for answer_item in answers:
        answer_item.total_correct_answers = 0
        answer_item.total_wrong_answers = 0
        answer_item.save()
    """
    return render(request, 'cdh_ecosystem_quiz/ftq_reset_scores.html')


# The functions are for the Multiple Choice Quiz



def multiple_choice_quiz(request):
    latest_question_list = Mc_Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'cdh_ecosystem_quiz/multiple_choice_quiz.html', context)


def multiple_choice_quiz_detail(request, question_id):
    question = get_object_or_404(Mc_Question, pk=question_id)
    return render(request, 'cdh_ecosystem_quiz/multiple_choice_quiz_detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Mc_Question, pk=question_id)
    try:
        selected_answer = question.mc_answer_set.get(pk=request.POST['answer'])
        user_selected_answer = smart_text(selected_answer)
        f = open('cdh_ecosystem_quiz/selected_answer.py', 'w')
        # the line below write the text 'user_response = ' and concats the user_response the str function gets rid of u in front of string
        f.write(str(user_selected_answer))
        f.close()
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'cdh_ecosystem_quiz/multiple_choice_quiz_detail.html', {
            'question': question,
            'error_message': "You didn't select an answer.",
        })
    else:
        selected_answer.votes += 1
        selected_answer.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # Note: cdh_ecosystem_quiz:multiple_choice_quiz_results calls the multiple_choice_quiz_results function
        context = {'selected_answer': selected_answer}
        return HttpResponseRedirect(reverse('cdh_ecosystem_quiz:multiple_choice_quiz_results', args=(question.id,)))
        #return redirect('cdh_ecosystem_quiz:multiple_choice_quiz_results', kwargs=(context, question_id))


def multiple_choice_quiz_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_selected_answer = ""
    f = open('cdh_ecosystem_quiz/selected_answer.py', 'rb')
    user_selected_answer = f.read()
    f.close()
    user_selected_answer = smart_text(user_selected_answer)
    answers = Mc_Answer.objects.filter(question_id=question.id)
    for answer in answers:
        correct_answer = answer.correct_answer
        image = answer.image
    image = str(answer.image)
    # Get the image "post_image/filename" for my_answer
    # Concatenates "/media/" + "post_image/filename"
    image = ("/media/" + (image))
    context = {'question': question, 'user_selected_answer': user_selected_answer,
    'correct_answer': correct_answer, 'image': image}
    return render(request, 'cdh_ecosystem_quiz/multiple_choice_quiz_results.html', context )





