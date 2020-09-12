from .models import Bot, BotHasQuestion
from django.forms import ModelForm


class BotCreationForm(ModelForm):
    class Meta:
        model = Bot
        fields = ('title', 'have_db', )
        labels = {
            'title': 'Название',
            'have_db': 'Используется ли бд'
        }


class BotHasQuestionAnswerForm(ModelForm):
    class Meta:
        model = BotHasQuestion
        fields = ('answer',)
        labels = {
            'answer': 'ответ',
        }
