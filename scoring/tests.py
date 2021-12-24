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
        data = {"candidate_ref": self.candidate_ref, "score": 10.3}
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
        data = {"candidate_ref": self.candidate_ref, "score": 10}
        response1 = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        response2 = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_error_if_score_out_of_range(self):
        data1 = {"candidate_ref": self.candidate_ref, "score": 103}
        response1 = self.client.post(
            "/create-score", data1, content_type="application/json"
        )
        data2 = {"candidate_ref": self.candidate_ref, "score": -3}
        response2 = self.client.post(
            "/create-score", data2, content_type="application/json"
        )        
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_error_on_inexistent_ref(self):
        data = {"candidate_ref": "87654321", "score": 10}
        response = self.client.post(
            "/create-score", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_error_on_bad_method(self):
        response = self.client.get("/create-score")
        self.assertEqual(response.status_code, 405)

    def test_error_on_bad_json(self):
        data = {"not-an-identifier": "12345678", "score": 10}
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


class GetCandidateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.candidate_ref = "ref12345"
        self.candidate_name = "foo"

    def test_can_retrieve_candidate_and_multiple_scores(self):
        self.client.post(
            "/create-candidate",
            {"ref": self.candidate_ref, "name": self.candidate_name},
            content_type="application/json"
        )
        scores = [score1 := 10, score2 := 55]
        data1 = {"candidate_ref": self.candidate_ref, "score": score1}
        self.client.post(
            "/create-score", data1, content_type="application/json"
        )
        data2 = {"candidate_ref": self.candidate_ref, "score": score2}
        self.client.post(
            "/create-score", data2, content_type="application/json"
        )
        response = self.client.get(f"/get-candidate/{self.candidate_ref}")
        body = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["candidate_ref"], self.candidate_ref)
        self.assertEqual(body["name"], self.candidate_name)
        self.assertEqual({float(x) for x in body["scores"]}, set(scores))

    def test_error_on_inexistent_candidate(self):
        response = self.client.get(f"/get-candidate/876532A")
        self.assertEqual(response.status_code, 400)

    def test_error_on_bad_method(self):
        response = self.client.post("/get-candidate/12345678")
        self.assertEqual(response.status_code, 405)
