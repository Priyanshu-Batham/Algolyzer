from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    # Personal Information
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        blank=True,
        null=True,
    )
    address = models.TextField(blank=True, null=True)

    # Ranking System
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username

    def add_xp(self, amount):
        """Add XP and check for level up"""
        self.xp += amount
        self.check_level_up()
        self.save()

    def check_level_up(self):
        """Update level based on XP thresholds"""
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
        # If user has more exp than our thresholds itself then dynamically create new thresholds
        while len(level_thresholds) <= self.level:
            level_thresholds.append(
                level_thresholds[-1] + (self.level * 500)
            )  # Custom scaling

        for i, threshold in enumerate(level_thresholds):
            if self.xp >= threshold:
                self.level = i + 1

    def get_next_level_xp(self):
        """Returns XP required for the next level"""
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
        if self.level < len(level_thresholds):
            return level_thresholds[self.level] - self.xp
        return None  # If max level is reached
