import json

from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError

from .models import Candidate, Score


CREATE_CANDIDATE_BAD_JSON_ERR_MSG = "The request JSON must be of the form: " +\
    "{'ref': <ref>, 'name': <name>}"

def create_candidate(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
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
    else:
        error_msg = bad_method("create_candidate", "POST", request.method)
        return JsonResponse({"errors": [error_msg]}, status=405)


def create_score(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"Hi!"})


def bad_method(resource: str, expected: str, actual: str) -> str:
    return f"Expected method '{expected}' for {resource} but got '{actual}'"
