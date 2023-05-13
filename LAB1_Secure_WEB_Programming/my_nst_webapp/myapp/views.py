from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm


class IndexView(generic.ListView):
    template_name = "myapp/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "myapp/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "myapp/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "myapp/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("myapp:results", args=(question.id,)))


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]

        if form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            question = form.save()
            for cf in choice_forms:
                choice = cf.save(commit=False)
                choice.question = question
                choice.save()
            return redirect('myapp:index')
    else:
        form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=str(x)) for x in range(0, 3)]

    return render(request, 'myapp/add_question.html', {'form': form, 'choice_forms': choice_forms})
