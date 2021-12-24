"""
Views corresponding to the three endpoints:

  - POST /create-candidate
  - POST /create-score
  - GET /get-candidate/<ref>
"""
import json
from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError

from .models import Candidate, Score


CREATE_CANDIDATE_BAD_JSON_ERR_MSG = "The request JSON must be of the form: " +\
    "{'ref': <ref>, 'name': <name>}"
CREATE_SCORE_BAD_JSON_ERR_MSG = "The request JSON must be of the form: " +\
    "{'candidate-ref': <ref>, 'score': <score>}"
View = Callable[[HttpRequest, ...], HttpResponse]


def accept_http_method(accepted: str) -> Callable[[str], Callable[[View], View]]:
    """Return a function wrapping func that returns an error if the
    HTTP method does not match accepted.

    Keyword arguments:
    func -- the function to wrap
    accepted -- the accepted HTTP method
    """
    def decorate(func: Callable[[HttpRequest], HttpResponse]):
        def wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            if request.method == accepted:
                return func(request, *args, **kwargs)
            name = func.__name__
            error_msg = f"Expected method '{accepted}' for {name}" +\
                f"but got '{request.method}'"
            return JsonResponse({"errors": [error_msg]}, status=405)
        return wrapped
    return decorate


@accept_http_method("POST")
def create_candidate(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        candidate = Candidate(ref=data["ref"], name=data["name"])
        candidate.full_clean()
    except (KeyError, json.JSONDecodeError):
        return JsonResponse(
            {"errors": [CREATE_CANDIDATE_BAD_JSON_ERR_MSG]}, status=400
        )
    except ValidationError as e:
        return JsonResponse({"errors": [str(e)]}, status=400)
    else:
        candidate.save()
        return JsonResponse(data)


@accept_http_method("POST")
def create_score(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        ref, score_val = data["candidate_ref"], data["score"]
        candidate = Candidate.objects.filter(ref=ref).first()
        if candidate is None:
            error_msg = f"No candidate found with ref '{ref}'"
            return JsonResponse({"errors": [error_msg]}, status=400)
        else:
            score = Score(candidate=candidate, score=float(score_val))
        score.full_clean()
    except (KeyError, json.JSONDecodeError):
        return JsonResponse(
            {"errors": [CREATE_SCORE_BAD_JSON_ERR_MSG]}, status=400
        )
    except ValueError:
        error_msg = f"Expected float for score but found: '{score_val}'"
        return JsonResponse({"errors": [error_msg]}, status=400)
    except ValidationError as e:
        return JsonResponse({"errors": [str(e)]}, status=400)
    else:
        score.save()
        return JsonResponse(data)


@accept_http_method("GET")
def get_candidate(_: HttpRequest, ref: str) -> JsonResponse:
    try:
        candidate = Candidate.objects.filter(ref=ref).first()
        if candidate is None:
            error_msg = f"No candidate found with ref '{ref}'"
            return JsonResponse({"errors": [error_msg]}, status=400)
        scores_query = Score.objects.values_list("score", flat=True)
        scores = list(scores_query.filter(candidate=candidate))
    except ValidationError as e:
        return JsonResponse({"errors": [str(e)]}, status=400)
    else:
        return JsonResponse(
            {"candidate_ref": ref, "name": candidate.name, "scores": scores}
        )
