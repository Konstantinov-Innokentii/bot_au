from django.urls import path

from .views import BotDetailView, BotCreateView, BotHasQuestionUpdateView, BotListView, BotResultView, \
    RedirectToMainView

urlpatterns = [
    path('bots/', BotListView.as_view(), name='bots'),
    path('bots/new/', BotCreateView.as_view(), name='bot_new'),
    path('bots/<int:pk>/', BotDetailView.as_view(), name='bot_detail'),
    path('bots/<int:pk>/result', BotResultView.as_view(), name='bot_result'),
    path('answer/<int:pk>/', BotHasQuestionUpdateView.as_view(), name='answer'),
    path('', RedirectToMainView.as_view(), name='redirect_to_main')
]
