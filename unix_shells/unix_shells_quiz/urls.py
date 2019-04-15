from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'unix_shells_quiz'
urlpatterns = [
# About page located at /unix_shells_quiz/unix_shells_quiz/index.html
path('', views.index, name='index'),

path('account/', include('registration.backends.default.urls')),
# Registration page
path('account/register/', include('registration.backends.default.urls')),
# Login page
path('account/login/', include('registration.backends.default.urls')),
# Logout page
path('logout/', views.logout, name='logout'),


# Quiz_Selection page
path('quiz_selection/', views.quiz_selection, name='quiz_selection'),
# Short Answer Quiz Categories page
path('short_answer_quiz_categories/', views.short_answer_quiz_categories, name='short_answer_quiz_categories'),
#
path('quiz/', views.quiz, name='index'),
# Resources page
path('resources/', views.git_resources, name='resources'),


# Short Answer Quiz detail page
re_path(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
# Short Answer Quiz results page
re_path(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
# Short Answer Quiz reset scores page
re_path(r'^reset_scores/', views.reset_scores, name='reset_scores'),
# Quiz page
re_path(r'^quiz/$', views.quiz, name='index'),


# Multiple Choice quiz
path('multiple_choice_quiz/', views.multiple_choice_quiz, name='multiple_choice_quiz'),
# Multiple Choice quiz detail page
re_path(r'^multiple_choice_quiz/(?P<question_id>[0-9]+)/$', views.multiple_choice_quiz_detail, name='multiple_choice_quiz_detail'),
# Multiple Choice vote page
re_path(r'^multiple_choice_quiz/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# Multiple Choice vote page
re_path(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# Multiple Choice results page
re_path(r'^(?P<question_id>[0-9]+)/vote/results/$', views.multiple_choice_quiz_results, name='multiple_choice_quiz_results'),


# Feynman Technique
path('feynman_technique_quiz/', views.feynman_technique_quiz, name='feynman_technique_quiz'),
# Feynman Technique FTQ detail page
re_path(r'^feynman_technique_quiz/(?P<question_id>[0-9]+)/$', views.ftq_detail, name='ftq_detail'),
# Feynman Technique FTQ results pages
re_path(r'^feynman_technique_quiz/(?P<question_id>[0-9]+)/results/$', views.ftq_results, name='ftq_results'),
# Feynman Technique Quiz reset scores
re_path(r'^feynman_technique_quiz/reset_scores/$', views.ftq_reset_scores, name='ftq_reset_scores'),


# Short Answer Quiz detail page
re_path(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
# Short Answer Quiz results page
re_path(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
# Short Answer Quiz reset scores page
re_path(r'^reset_scores/', views.reset_scores, name='reset_scores'),
# Quiz page
re_path(r'^quiz/$', views.quiz, name='index'),


# Note: the answers url is not being used in the app but is left here
# as an example for future versions
#    url(r'^(?P<question_id>[0-9]+)/answer/$', views.answer, name='answer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

