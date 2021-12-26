"""
Views corresponding to the three endpoints:

  - POST /create-candidate
  - POST /create-score
  - GET /get-candidate/<ref>
"""
import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views import View

from .models import Candidate, Score


class CreateCandidateView(View):

    create_candidate_bad_json_err_msg = "The request JSON must be of the" +\
        " form: {'ref': <ref>, 'name': <name>}"

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
            candidate = Candidate(ref=data["ref"], name=data["name"])
            candidate.full_clean()
        except (KeyError, json.JSONDecodeError):
            return JsonResponse(
                {"errors": self.create_candidate_bad_json_err_msg}, status=400
            )
        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)
        else:
            candidate.save()
            # The spec doesn't specify, but we return the candidate back anyway
            return JsonResponse(data)


class CreateScoreView(View):

    create_score_bad_json_err_msg = "The request JSON must be of the" +\
        " form: {'candidate-ref': <ref>, 'score': <score>}"

    def post(self, request: HttpRequest) -> JsonResponse:
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
                {"errors": [self.create_score_bad_json_err_msg]}, status=400
            )
        except ValueError:
            error_msg = f"Expected float for score but found: '{score_val}'"
            return JsonResponse({"errors": [error_msg]}, status=400)
        except ValidationError as e:
            return JsonResponse({"errors": e.message_dict}, status=400)
        else:
            score.save()
            return JsonResponse(data)


class GetCandidateView(View):

    def get(self, _: HttpRequest, ref: str) -> JsonResponse:
        candidate = Candidate.objects.filter(ref=ref).first()
        if candidate is None:
            error_msg = f"No candidate found with ref '{ref}'"
            return JsonResponse(
                {"errors": {"candidate": error_msg}}, status=400)
        scores_query = Score.objects.values_list("score", flat=True)
        scores = list(scores_query.filter(candidate=candidate))
        return JsonResponse(
            {"candidate_ref": ref, "name": candidate.name, "scores": scores}
        )
