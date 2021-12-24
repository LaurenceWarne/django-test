from django.db import models
from django.core.validators import RegexValidator


CANDIDATE_PKEY_VALIDATOR = RegexValidator(
    r"[0-9a-zA-z]{8}",
    "Candidate Reference should be a unique string of 8 letters and digits"
)

class Candidate(models.Model):
    ref = models.CharField(
        primary_key=True, validators=[CANDIDATE_PKEY_VALIDATOR]
    )
    name = models.TextField()


class Score(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.FloatField()
