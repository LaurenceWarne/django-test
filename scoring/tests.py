import json

from django.test import Client, TestCase


class CreateCandidateTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_can_create_candidate(self):
        data = {"ref": "12345678", "name": "foo"}
        response = self.client.post(
            "/create-candidate", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_error_on_bad_ref(self):
        data = {"ref": "not a valid ref", "name": "foo"}
        response = self.client.post(
            "/create-candidate", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_error_on_bad_method(self):
        response = self.client.get("/create-candidate")
        self.assertEqual(response.status_code, 405)

    def test_error_on_bad_json(self):
        data = {"not-an-identifier": "12345678", "name": "foo"}
        response = self.client.post(
            "/create-candidate", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class CreateScoreTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.candidate_ref = "score123"

    def test_can_create_score(self):
        self.client.post(
            "/create-candidate",
            {"ref": self.candidate_ref, "name": "foo"},
            content_type="application/json"
        )
        data = {"candidate_ref": self.candidate_ref, "score": "10"}
        response = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_can_create_multiple_scores_for_candidate(self):
        self.client.post(
            "/create-candidate",
            {"ref": self.candidate_ref, "name": "foo"},
            content_type="application/json"
        )
        data = {"candidate_ref": self.candidate_ref, "score": "10"}
        response1 = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        response2 = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_error_on_inexistant_ref(self):
        data = {"candidate_ref": "87654321", "score": "10"}
        response = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_error_on_bad_method(self):
        response = self.client.get("/create-score")
        self.assertEqual(response.status_code, 405)

    def test_error_on_bad_json(self):
        data = {"not-an-identifier": "12345678", "score": "10"}
        response = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_error_on_bad_float(self):
        data = {"candidate_ref": self.candidate_ref, "score": "abc"}
        response = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        
