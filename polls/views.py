from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from .forms import QuestionForm
from django.contrib import messages

def index(request):
	latest_question=Question.objects.all()
	#output='<br>'.join([q.question_text for q in latest_question])
	#return HttpResponse(output)
	context={'latest_question_list':latest_question}
	return render(request,'polls/index.html',context)


def detail(request,question_id):
	#return HttpResponse(f"<h3>You're looking at question {question_id}</h3>")
	try:
		question=Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question doen not exist!")
	ctx={'question': question}
	return render(request,'polls/detail.html',ctx)

def results(request,question_id):
	#return HttpResponse(f"<h3>You're looking at result of question {question_id}</h3>")
	question=get_object_or_404(Question,pk=question_id)
	return render(request, 'polls/results.html',{'question':question})

def vote(request,question_id):
	#return HttpResponse(f"<h3>You're voting on question {question_id}</h3>")
	question=get_object_or_404(Question, pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'polls/detail.html',{'question':question,
								'error_message':"You didn't select a choice!",})
	else:
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

def add_question(request):
	if request.method=='POST':
		question = QuestionForm(request.POST)
		if question.is_valid():
			question.save()
			messages.info(request,'Question Added successfully!')
			return HttpResponseRedirect(reverse("polls:index"))
		else:
			messages.info(request,'Invalid Data!')
			return HttpResponseRedirect(reverse("polls:add_question"))
	else:
		question=QuestionForm()
		return render(request,'polls/add_question.html',{'question':question})