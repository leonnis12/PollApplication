from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponse,  JsonResponse, HttpResponseRedirect
from django.core import serializers
from .forms import CreatePollForm, CreateQuizForm
from .models import Poll, Quiz
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    polls = Poll.objects.filter(quiz__isnull=True)
    quizes = Quiz.objects.all()

    context={}
    if "HTTP_REFERER" in request.META and "quiz" in request.META["HTTP_REFERER"] and request.session.get('finished') == "quiz":
        context['finished_text']="You have finished your quiz. Tip: You can create one yourself on the create pacge."
        del request.session['finished']
        request.session.modified = True
    if "HTTP_REFERER" in request.META and "create" in request.META["HTTP_REFERER"] and request.session.get('created') == "quiz":
        context['finished_text']="Quiz was created."
        del request.session['created']
        request.session.modified = True
    if "HTTP_REFERER" in request.META and "create" in request.META["HTTP_REFERER"] and request.session.get('created') == "poll":
        context['finished_text']="Poll was created."
        del request.session['created']
        request.session.modified = True
    request.session.get("false")

    context ['polls']=polls
    context ['quizes']=quizes

    return render(request, 'poll/home.html', context)

class ResultView(DetailView):
    model = Poll
    template_name = "poll/results.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context
    
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if 'polls_voted' not in request.session:
        request.session['polls_voted']=[]
        request.session.modified = True
    if poll.pk in request.session['polls_voted']:
        return redirect('results', poll.id)

    if request.method == 'POST':
        # check for already completed poll
        if poll.pk not in request.session['polls_voted']:
            request.session['polls_voted'].append(poll.pk)
            request.session.modified = True
        else:
            return redirect('results', poll.id)

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

        poll.save()
        return redirect('results', poll.id)

    context = {'poll' : poll}
    return render(request, 'poll/vote.html', context)

class QuizView(DetailView, MultipleObjectMixin):
    model = Quiz
    template_name = "poll/quiz.html"
    context_object_name = "quiz"
    paginate_by = 1

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.filter(pk=request.POST['poll_id']).first()

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

        poll.save()

        if int(request.POST['page_id'])+1 <= int(request.POST['pages_nr']): # Go to next page
            return redirect(str(self.request.path_info)+"?page="+str(int(request.POST['page_id'])+1))
        self.request.session['finished']= "quiz"
        # Finished pages
        return redirect("/")

    def get_context_data(self, **kwargs):
        object_list = Poll.objects.filter(quiz=next(iter(kwargs.values())).id)
        current_quiz = object_list
        context = super(QuizView, self).get_context_data(object_list=object_list, **kwargs)
        context['polls'] = object_list
        return context

def create(request):
    if request.method == 'POST':
        if "quiz_submit" in request.POST:
            form_quiz = CreateQuizForm(request.POST)
            if form_quiz.is_valid():
                quiz = form_quiz.save(commit=False)
                if request.user.is_authenticated:
                    quiz.author = request.user
                quiz.save()
                request.session['quiz_id'] = quiz.pk
                if request.is_ajax():
                    request.session['created']= "quiz"
                    return JsonResponse({"Received": True, "quiz_id": quiz.pk}, status=200)
                else:
                    return redirect('home')
            else:
                # some form errors occured.
                if request.is_ajax():
                    return JsonResponse({"error": form_quiz.errors}, status=400)
                else:
                    return redirect('home')
        elif "poll_submit" in request.POST:
            form_poll = CreatePollForm(request.POST)
            if form_poll.is_valid():
                poll = form_poll.save(commit=False)
                if request.user.is_authenticated:
                    poll.author = request.user
                if 'quiz_id' in request.session:
                    poll.quiz = Quiz.objects.get(id=request.session['quiz_id'])
                poll.save()
                if request.is_ajax():
                    return JsonResponse({"Received": True}, status=200)
                else:
                    request.session['created']= "poll"
                    return HttpResponseRedirect('/vote/%d/'%poll.id)
            else:
                # some form errors occured.
                if request.is_ajax():
                    return JsonResponse({"error": form_poll.errors}, status=400)
                else:
                    return redirect('home')
        else:
            return redirect('home')
    else:
        form_poll = CreatePollForm()
        form_quiz = CreateQuizForm()

    if 'quiz_id' in request.session:
        del request.session['quiz_id']
        request.session.modified = True
    context = {'form_poll' : form_poll, 'form_quiz' : form_quiz}
    return render(request, 'poll/create.html', context)