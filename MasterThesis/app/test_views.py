import pytest
from django.test import Client
from .forms import CreateNewList


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
class TestViews:
    """Tests for the application views."""

    def test_home(self, client):
        """Tests the home page."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Home Page" in response.content.decode()

    def test_contact(self, client):
        """Tests the contact page."""
        response = client.get("/contact/")
        assert response.status_code == 200
        assert "Contact" in response.content.decode()

    def test_about(self, client):
        """Tests the about page."""
        response = client.get("/about/")
        assert response.status_code == 200
        assert "About" in response.content.decode()

    def test_app(self, client):
        """Tests the app page."""
        response = client.get("/app/")
        assert response.status_code == 200
        assert "App" in response.content.decode()


class TestCreateNewListForm:
    def test_form_valid(self):
        data = {"Numerator": "1", "Denominator": "1"}
        form = CreateNewList(data=data)
        assert form.is_valid()

    def test_blank_input(self):
        form = CreateNewList(data={})
        assert not form.is_valid()
        assert "Numerator" in form.errors
        assert "Denominator" in form.errors

    def test_max_length_exceeded(self):
        data = {"Numerator": "1" * 21, "Denominator": "1" * 19}  # Exceeds max_length
        form = CreateNewList(data=data)
        assert not form.is_valid()
        assert "Numerator" in form.errors
        assert (
            "Ensure this value has at most 20 characters (it has 21)."
            in form.errors["Numerator"]
        )

    def test_valid_input(self):
        data = {"Numerator": "1", "Denominator": "1"}
        form = CreateNewList(data=data)
        assert form.is_valid()
