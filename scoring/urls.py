from django.urls import path

from . import views

urlpatterns = [
    path(
        "create-candidate",
        views.CreateCandidateView.as_view(),
        name="create_candidate"
    ),
    path(
        "create-score",
        views.CreateScoreView.as_view(),
        name="create_score"
    ),
    path(
        "get-candidate/<ref>",
        views.GetCandidateView.as_view(),
        name="get_candidate"
    )
]
