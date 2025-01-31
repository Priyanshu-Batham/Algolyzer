from django.contrib.auth import get_user_model
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="No description provided.")
    difficulty = models.CharField(
        max_length=7,
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
            ("Veteran", "Veteran"),
        ],
        default="Easy",
        help_text="Difficulty levels",
    )

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()  # The question text
    option_a = models.CharField(max_length=200)  # Option A
    option_b = models.CharField(max_length=200)  # Option B
    option_c = models.CharField(max_length=200)  # Option C
    option_d = models.CharField(max_length=200)  # Option D
    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("a", "Option A"),
            ("b", "Option B"),
            ("c", "Option C"),
            ("d", "Option D"),
        ],
        help_text="Correct answer should be 'a', 'b', 'c', or 'd'",
    )

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(
        max_length=1,
        choices=[
            ("a", "Option A"),
            ("b", "Option B"),
            ("c", "Option C"),
            ("d", "Option D"),
        ],
        help_text="Selected answer should be 'a', 'b', 'c', or 'd'",
    )
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "user",
            "topic",
            "question",
        )  # Ensure a user can only answer a question once in a topic

    def save(self, *args, **kwargs):
        # Automatically determine if the selected answer is correct
        self.is_correct = self.selected_answer == self.question.correct_answer
        super().save(*args, **kwargs)


class QuizProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
