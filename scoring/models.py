from django.db import models
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator
)


CANDIDATE_PKEY_VALIDATOR = RegexValidator(
    "^[0-9a-zA-z]{8}$",
    "Candidate Reference should be a unique string of 8 letters and digits"
)
SCORE_MIN_VALIDATOR = MinValueValidator(
    0,
    "A score cannot be less than zero"
)
SCORE_MAX_VALIDATOR = MaxValueValidator(
    100,
    "A score may not exceed 100"
)


class Candidate(models.Model):
    ref = models.CharField(
        primary_key=True, max_length=8, validators=[CANDIDATE_PKEY_VALIDATOR]
    )
    name = models.TextField()

    def __str__(self):
        return f"Candidate({self.ref}, {self.name})"


class Score(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )
    score = models.FloatField(
        validators=[SCORE_MIN_VALIDATOR, SCORE_MAX_VALIDATOR]
    )

    def __str__(self):
        return f"Score({self.candidate}, {self.score})"
