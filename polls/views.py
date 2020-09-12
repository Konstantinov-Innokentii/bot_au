from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Bot, BotHasQuestion
from .forms import BotCreationForm, BotHasQuestionAnswerForm


class BotHasQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = BotHasQuestion
    template_name = 'poll/bot_has_question_detail.html'
    form_class = BotHasQuestionAnswerForm

    def get_success_url(self):
        next_question = self.object.next()
        if next_question is not None:
            print("NOT YET")
            return reverse('answer', args=(next_question.pk,))
        else:
            print("END")
            return reverse('bot_result', args=(self.object.bot.pk,))


class BotCreateView(LoginRequiredMixin, CreateView):
    model = Bot
    form_class = BotCreationForm
    template_name = 'poll/bot_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        first_question = BotHasQuestion.objects.get(bot=self.object, order=0)
        return reverse('answer', args=(first_question.pk,))


class BotDetailView(LoginRequiredMixin, DetailView):
    model = Bot
    template_name = 'poll/bot_detail.html'


class BotResultView(LoginRequiredMixin, DetailView):
    model = Bot
    template_name = 'poll/bot_result.html'


class BotListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Bot.objects.filter(author=self.request.user)

    template_name = 'poll/bot_list.html'
