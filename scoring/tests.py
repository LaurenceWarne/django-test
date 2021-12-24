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
