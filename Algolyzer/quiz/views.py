from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from home.decorators import profile_required

from .forms import QuizForm
from .models import Question, QuizProgress, Topic, UserAnswer


@login_required
@profile_required
def quiz_home(request):
    """Main QUIZ Home Page"""
    data = []
    topics = Topic.objects.all()
    for topic in topics:
        score = 0
        total = Question.objects.filter(topic=topic).count()
        progress = QuizProgress.objects.filter(user=request.user, topic=topic).first()
        if progress is not None and progress.completed:
            answers = UserAnswer.objects.filter(user=request.user, topic=topic)
            score = answers.filter(is_correct=True).count()
        data.append(
            {
                "topic": topic,
                "score": score,
                "total": total,
            }
        )

    context = {"data": data}
    return render(request, "quiz/home.html", context=context)


@login_required
@profile_required
def quiz_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    score = 0
    total = 0
    progress = QuizProgress.objects.filter(user=request.user, topic=topic).first()
    if progress is not None and progress.completed:
        answers = UserAnswer.objects.filter(user=request.user, topic=topic)
        score = answers.filter(is_correct=True).count()
        total = Question.objects.filter(topic=topic).count()

    context = {
        "topic": topic,
        "score": score,
        "total": total,
    }
    return render(request, "quiz/topic.html", context=context)


@login_required
@profile_required
def quiz_start(request, topic_id):
    """
    Resets user progress to start a fresh quiz
    """
    topic = get_object_or_404(Topic, id=topic_id)
    questions = Question.objects.filter(topic=topic)
    if not questions.exists():
        return render(request, "quiz/no_questions.html")

    # Initialize or reset progress
    QuizProgress.objects.filter(user=request.user, topic=topic).delete()
    QuizProgress.objects.create(user=request.user, topic=topic, current_question=0)
    UserAnswer.objects.filter(user=request.user, topic=topic).delete()
    return redirect("quiz_question", topic_id=topic.id)


@login_required
@profile_required
def quiz_question(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    progress = get_object_or_404(QuizProgress, user=request.user, topic=topic)

    # Fetch the current question
    questions = Question.objects.filter(topic=topic)
    if progress.current_question >= len(questions):
        progress.completed = True
        progress.save()
        return redirect("quiz_results", topic_id=topic.id)

    question = questions[progress.current_question]

    if request.method == "POST":
        form = QuizForm(question, request.POST)
        if form.is_valid():
            selected_answer = form.cleaned_data["answer"]

            # Save user's answer, is_correct field is managed internally in model.
            UserAnswer.objects.create(
                topic=topic,
                user=request.user,
                question=question,
                selected_answer=selected_answer,
            )

            # Move to the next question
            progress.current_question += 1
            progress.save()
            return redirect("quiz_question", topic_id=topic.id)
    else:
        form = QuizForm(question)

    return render(
        request,
        "quiz/question.html",
        {"form": form, "progress": progress, "total_array": range(len(questions))},
    )


@login_required
@profile_required
def quiz_results(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quiz_progress = get_object_or_404(QuizProgress, topic=topic, user=request.user)
    if not quiz_progress.completed:
        return redirect("quiz_question", topic_id=topic.id)
    answers = UserAnswer.objects.filter(user=request.user, topic=topic)
    score = answers.filter(is_correct=True).count()
    total = Question.objects.filter(topic=topic).count()

    context = {
        "topic": topic,
        "score": score,
        "total": total,
    }

    return render(request, "quiz/results.html", context=context)
