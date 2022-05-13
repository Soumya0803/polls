from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question,Choice
from django.template import loader
from .forms import PollsForm, ChoiceForm
from django.forms import modelformset_factory, inlineformset_factory
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
       
def get_polls(request):

        form = PollsForm(request.POST)
        ChoiceFormSet = inlineformset_factory(Question, Choice, form= ChoiceForm,fields=('choice_text',),extra=7,min_num=3,max_num=10)
        choiceformset = ChoiceFormSet()
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.instance.pub_date= timezone.now()
            ques_form=form.save()

            ques = Question.objects.get(id=ques_form.pk)
            choiceformset = ChoiceFormSet(request.POST,instance=ques)

        if  choiceformset.is_valid():
            print('flag')
            choice_form=choiceformset.save()
            return redirect('polls:index')

        return render(request, 'polls/pollsform.html', {'form': form, 'choiceformset': choiceformset})
