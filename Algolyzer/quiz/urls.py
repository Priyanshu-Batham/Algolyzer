from django.urls import path

from .views import quiz_home, quiz_question, quiz_results, quiz_start, quiz_topic

urlpatterns = [
    path("", quiz_home, name="quiz_home"),
    path("topic/<int:topic_id>/", quiz_topic, name="quiz_topic"),
    path("start/<int:topic_id>/", quiz_start, name="quiz_start"),
    path("question/<int:topic_id>/", quiz_question, name="quiz_question"),
    path("results/<int:topic_id>/", quiz_results, name="quiz_results"),
]
