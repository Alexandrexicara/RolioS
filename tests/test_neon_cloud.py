import unittest
from unittest.mock import Mock

from rollos.neon_cloud import NeonProvisioner, NeonProvisioningError


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload
        self.status_code = status
        self.ok = status < 400

    def json(self):
        return self.payload


class NeonProvisionerTests(unittest.TestCase):
    def test_lists_organizations(self):
        session = Mock()
        session.request.return_value = FakeResponse({
            "organizations": [{"id": "org-123", "name": "Minha conta"}]
        })
        client = NeonProvisioner("secret-test-key", session=session)
        self.assertEqual(
            client.list_organizations(),
            [{"id": "org-123", "name": "Minha conta"}],
        )
        headers = session.request.call_args.kwargs["headers"]
        self.assertEqual(headers["Authorization"], "Bearer secret-test-key")

    def test_creates_project_and_extracts_uri(self):
        session = Mock()
        session.request.return_value = FakeResponse({
            "project": {"id": "quiet-tree-123", "name": "rollos-user", "region_id": "aws-us-east-1"},
            "connection_uris": [{"connection_uri": "postgresql://user:secret@host/db"}],
        }, status=201)
        client = NeonProvisioner("secret-test-key", session=session)
        project = client.create_project("org-123", "rollos-user")
        self.assertEqual(project.project_id, "quiet-tree-123")
        self.assertEqual(project.connection_uri, "postgresql://user:secret@host/db")
        payload = session.request.call_args.kwargs["json"]
        self.assertEqual(payload["project"]["branch"]["database_name"], "rollos")
        self.assertEqual(payload["org_id"], "org-123")

    def test_rejects_unsupported_region_before_request(self):
        session = Mock()
        client = NeonProvisioner("secret-test-key", session=session)
        with self.assertRaises(ValueError):
            client.create_project("org-123", region_id="unknown-region")
        session.request.assert_not_called()

    def test_reports_api_error_without_retrying_create(self):
        session = Mock()
        session.request.return_value = FakeResponse({"message": "permission denied"}, status=403)
        client = NeonProvisioner("secret-test-key", session=session)
        with self.assertRaises(NeonProvisioningError):
            client.create_project("org-123")
        self.assertEqual(session.request.call_count, 1)


if __name__ == "__main__":
    unittest.main()
