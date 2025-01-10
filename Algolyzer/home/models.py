from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    dob = models.DateField()
    # fields for ranking system
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username

    def add_xp(self, amount):
        self.xp += amount
        self.check_level_up()

    def check_level_up(self):
        # Example level thresholds (customize as needed)
        level_thresholds = [0, 100, 300, 600, 1000]  # XP required for each level
        for i, threshold in enumerate(level_thresholds):
            if self.xp >= threshold:
                self.level = i + 1
        self.save()
