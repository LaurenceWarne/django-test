from django.http import HttpResponse


def create_score(request) -> HttpResponse:
    return HttpResponse("Hi!")
