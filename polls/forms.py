from .models import Bot, BotHasQuestion
from django.forms import ModelForm, ValidationError


class BotCreationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bot
        fields = ('title', 'have_db', )
        labels = {
            'title': 'Название',
            'have_db': 'Используется ли бд'
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if self.current_user.bots.filter(title=title).exists():
            raise ValidationError("Бот с таким именем существует.")
        return title


class BotHasQuestionAnswerForm(ModelForm):
    class Meta:
        model = BotHasQuestion
        fields = ('answer',)
        labels = {
            'answer': 'ответ',
        }
