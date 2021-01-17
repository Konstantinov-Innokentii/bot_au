from django.forms import ModelForm, ValidationError, BooleanField

from .models import Bot, BotHasQuestion


class BotCreationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bot
        fields = ('title', 'have_db',)
        labels = {
            'title': 'Название',
            'have_db': 'Используется ли БД в вашем боте?'
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if self.current_user.bots.filter(title=title).exists():
            raise ValidationError("Бот с таким именем существует.")
        return title


class BotHasQuestionAnswerForm(ModelForm):
    class Meta:
        model = BotHasQuestion
        fields = ()

    yes = BooleanField(initial=False, required=False, label="Да")
    no = BooleanField(initial=False, required=False, label="Нет")

    def clean(self):
        yes = self.cleaned_data["yes"]
        no = self.cleaned_data["no"]
        if yes == no:
            raise ValidationError("Выберите один ответ.")
