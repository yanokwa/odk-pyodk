from unittest import TestCase
from unittest.mock import MagicMock, patch

from pyodk.client import Client
from pyodk.endpoints.forms import Form
from pyodk.session import Session
from tests.resources import CONFIG_DATA, forms_data


@patch("pyodk.client.Client._login", MagicMock())
@patch("pyodk.config.read_config", MagicMock(return_value=CONFIG_DATA))
class TestForms(TestCase):
    def test_read_all__ok(self):
        """Should return a list of FormType objects."""
        fixture = forms_data.test_forms
        with patch.object(Session, "request") as mock_session:
            mock_session.return_value.status_code = 200
            mock_session.return_value.json.return_value = fixture["response_data"]
            with Client() as client:
                observed = client.forms.list()
        self.assertEqual(4, len(observed))
        for i, o in enumerate(observed):
            with self.subTest(i):
                self.assertIsInstance(o, Form)

    def test_read__ok(self):
        """Should return a FormType object."""
        fixture = forms_data.test_forms
        with patch.object(Session, "request") as mock_session:
            mock_session.return_value.status_code = 200
            mock_session.return_value.json.return_value = fixture["response_data"][0]
            with Client() as client:
                # Specify project
                observed = client.forms.get(
                    project_id=fixture["project_id"],
                    form_id=fixture["response_data"][0]["xmlFormId"],
                )
                self.assertIsInstance(observed, Form)
                # Use default
                observed = client.forms.get(
                    form_id=fixture["response_data"][0]["xmlFormId"]
                )
                self.assertIsInstance(observed, Form)
