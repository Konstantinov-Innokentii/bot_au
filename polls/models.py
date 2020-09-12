from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ordered_model.models import OrderedModel


class Bot(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="bots", null=False)
    have_db = models.BooleanField()
    result = models.IntegerField(default=None, null=True)

    @property
    def res(self):
        all_questions = BotHasQuestion.objects.filter(bot=self)
        no_questions = BotHasQuestion.objects.filter(bot=self, answer=False)
        total_sum = 0
        for q in all_questions:
            total_sum += q.question.weight
        n_sum = 0
        for n_q in no_questions:
            n_sum += n_q.question.weight
        return round(100 - n_sum/total_sum * 100)

    @property
    def improvements(self):
        return list(BotHasQuestion.objects.filter(bot=self, answer=False))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_title_author')
        ]

    questions = models.ManyToManyField("Question", through="BotHasQuestion")


class Question(models.Model):
    text = models.CharField(max_length=250)
    WEIGHT_CHOICES = [(i, i) for i in range(11)]
    weight = models.IntegerField(choices=WEIGHT_CHOICES)
    solution = models.TextField(null=True, default=None)
    db = models.BooleanField()
    threat = models.CharField(max_length=250, null=True, default=None)
    verbal = models.CharField(max_length=250, null=True, default=None)
    link = models.URLField(null=True, default=None)

    def __str__(self):
        return f"{self.text}"


class BotHasQuestion(OrderedModel):
    order_with_respect_to = ("bot", )
    bot = models.ForeignKey(
        "Bot",
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
    )

    answer = models.BooleanField(default=False)

    class Meta:
        unique_together = ('bot', 'question')


@receiver(post_save, sender=Bot)
def listen_for_bot_model_save(sender, instance, created, *args, **kwargs):
    if created:
        for question in Question.objects.all():
            BotHasQuestion.objects.create(question=question, bot=instance)
