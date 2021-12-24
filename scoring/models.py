from django.db import models
from django.core.validators import RegexValidator


CANDIDATE_PKEY_VALIDATOR = RegexValidator(
    "^[0-9a-zA-z]{8}$",
    "Candidate Reference should be a unique string of 8 letters and digits"
)

class Candidate(models.Model):
    ref = models.CharField(
        primary_key=True, max_length=8, validators=[CANDIDATE_PKEY_VALIDATOR]
    )
    name = models.TextField()

    def __str__(self):
        return f"Candidate({self.ref}, {self.name})"


class Score(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"Score({self.candidate}, {self.score})"
