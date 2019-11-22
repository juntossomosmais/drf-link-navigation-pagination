import json

import pytest
from rest_framework import status
from tests.support.fake_django_app.models import TestModel


@pytest.fixture(autouse=True)
def setup_for_each_test():
    for n in range(1, 201):
        TestModel.objects.create(some_integer=n)


@pytest.mark.django_db
def test_should_receive_updated_url_for_next_given_custom_domain(client):
    custom_domain = "salted-man"
    custom_limit = 2
    response = client.get(f"/data/?limit={custom_limit}", HTTP_X_DRF_CHANGE_DOMAIN=custom_domain)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "count": 200,
        "next": f"https://{custom_domain}/data/?limit={custom_limit}&offset=2",
        "previous": None,
        "results": [{"id": 1, "some_integer": 1}, {"id": 2, "some_integer": 2}],
    }


@pytest.mark.django_db
def test_should_receive_updated_url_for_next_and_previous_given_custom_domain(client):
    custom_domain = "salted-man"
    custom_limit = 2

    response = client.get(f"/data/?limit={custom_limit}", HTTP_X_DRF_CHANGE_DOMAIN=custom_domain)
    response = client.get(response.data["next"].split(custom_domain)[1], HTTP_X_DRF_CHANGE_DOMAIN=custom_domain)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "count": 200,
        "next": f"https://{custom_domain}/data/?limit={custom_limit}&offset=4",
        "previous": f"https://{custom_domain}/data/?limit={custom_limit}",
        "results": [{"id": 3, "some_integer": 3}, {"id": 4, "some_integer": 4}],
    }


@pytest.mark.django_db
def test_should_not_receive_updated_url_for_next_given_no_custom_domain_is_set(client):
    response = client.get(f"/data/")

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "count": 200,
        "next": "http://testserver/data/?limit=5&offset=5",
        "previous": None,
        "results": [
            {"id": 1, "some_integer": 1},
            {"id": 2, "some_integer": 2},
            {"id": 3, "some_integer": 3},
            {"id": 4, "some_integer": 4},
            {"id": 5, "some_integer": 5},
        ],
    }


@pytest.mark.django_db
def test_should_not_receive_updated_url_for_next_and_previous_given_no_custom_domain_is_set(client):
    response = client.get(f"/data/")
    response = client.get(response.data["next"].split("testserver")[1])

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "count": 200,
        "next": "http://testserver/data/?limit=5&offset=10",
        "previous": "http://testserver/data/?limit=5",
        "results": [
            {"id": 6, "some_integer": 6},
            {"id": 7, "some_integer": 7},
            {"id": 8, "some_integer": 8},
            {"id": 9, "some_integer": 9},
            {"id": 10, "some_integer": 10},
        ],
    }
