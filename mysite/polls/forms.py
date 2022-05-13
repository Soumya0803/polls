from django.forms import ModelForm
from polls.models import Question, Choice


class PollsForm(ModelForm):
    class Meta:
        model =  Question
        fields = ['question_text']
    # question = forms.CharField(label='Question', max_length=2000)
    # option1 = forms.CharField(label='Option1', max_length=100)
    # option2 = forms.CharField(label='Option2', max_length=100)
    # option3 = forms.CharField(label='Option3', max_length=100)
    
class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']