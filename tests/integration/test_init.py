import json

import pytest
from rest_framework import status

from drf_link_navigation_pagination import _overlap_path
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
        "next": f"http://{custom_domain}/data/?limit={custom_limit}&offset=2",
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
        "next": f"http://{custom_domain}/data/?limit={custom_limit}&offset=4",
        "previous": f"http://{custom_domain}/data/?limit={custom_limit}",
        "results": [{"id": 3, "some_integer": 3}, {"id": 4, "some_integer": 4}],
    }


@pytest.mark.django_db
def test_should_receive_updated_url_for_next_given_custom_request_path_with_https_or_http(client):
    custom_request_path = "salted-path"
    headers = {"HTTP_X_DRF_ADD_REQUEST_PATH": custom_request_path}

    def _do_execute_and_assert(with_https: bool):
        custom_headers = {"HTTP_X_DRF_FORCE_HTTPS": with_https}
        custom_headers.update(headers)
        scheme = "https" if with_https else "http"

        response = client.get(f"/data/?limit=1", **custom_headers)
        assert response.status_code and json.loads(response.content) == {
            "count": 200,
            "next": f"{scheme}://testserver/{custom_request_path}/data?limit=1&offset=1",
            "previous": None,
            "results": [{"id": 1, "some_integer": 1}],
        }

        response = client.get(f"/data/?limit=1", **custom_headers)
        assert response.status_code and json.loads(response.content) == {
            "count": 200,
            "next": f"{scheme}://testserver/{custom_request_path}/data?limit=1&offset=1",
            "previous": None,
            "results": [{"id": 1, "some_integer": 1}],
        }

        response = client.get(f"/data/?limit=1", **custom_headers)
        assert response.status_code and json.loads(response.content) == {
            "count": 200,
            "next": f"{scheme}://testserver/{custom_request_path}/data?limit=1&offset=1",
            "previous": None,
            "results": [{"id": 1, "some_integer": 1}],
        }

        response = client.get(f"/data/?limit=1", **custom_headers)
        assert response.status_code and json.loads(response.content) == {
            "count": 200,
            "next": f"{scheme}://testserver/{custom_request_path}/data?limit=1&offset=1",
            "previous": None,
            "results": [{"id": 1, "some_integer": 1}],
        }

    _do_execute_and_assert(with_https=True)
    _do_execute_and_assert(with_https=False)


@pytest.mark.django_db
def test_should_receive_updated_url_for_next_given_custom_request_path_and_domain(client):
    custom_domain = "salted-man"
    custom_request_path = "salted-path"
    headers = {"HTTP_X_DRF_ADD_REQUEST_PATH": custom_request_path, "HTTP_X_DRF_CHANGE_DOMAIN": custom_domain}

    response = client.get(f"/data/?limit=1", **headers)
    assert response.status_code and json.loads(response.content) == {
        "count": 200,
        "next": f"http://{custom_domain}/{custom_request_path}/data?limit=1&offset=1",
        "previous": None,
        "results": [{"id": 1, "some_integer": 1}],
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


@pytest.mark.django_db
def test_should_receive_update_url_for_next_overlapping_path(client):
    headers = {"HTTP_X_DRF_NUMBER_OVERLAP_PATHS": 1}

    response = client.get(f"/data/?limit=1", **headers)
    assert response.status_code and json.loads(response.content) == {
        "count": 200,
        "next": "http://testserver/?limit=1&offset=1",
        "previous": None,
        "results": [{"id": 1, "some_integer": 1}],
    }


@pytest.mark.django_db
def test_should_overlap_3_paths():
    assert _overlap_path("http://testserver/first/second/third/fourth/", 1) == "http://testserver/second/third/fourth/"
    assert _overlap_path("http://testserver/first/second/third/fourth/", 2) == "http://testserver/third/fourth/"
    assert _overlap_path("http://testserver/first/second/third/fourth/", 3) == "http://testserver/fourth/"
    assert (
        _overlap_path("http://testserver/first/second/third/fourth/fifth/?limit=1&offset=1", 4)
        == "http://testserver/fifth/?limit=1&offset=1"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "pagination_size,limit,expected_status",
    [
        (10, 10, status.HTTP_200_OK),
        (10, 1, status.HTTP_200_OK),
        (10, 11, status.HTTP_400_BAD_REQUEST),
        # defaults to default limit (aka the page size on the settings)
        (10, -1, status.HTTP_200_OK),
        (20, 11, status.HTTP_200_OK),
        (20, 21, status.HTTP_400_BAD_REQUEST),
        (None, 200, status.HTTP_200_OK)
    ],
)
def test_should_set_max_limit_if_received_the_header(client, pagination_size, limit, expected_status):
    headers = {"HTTP_X_DRF_MAX_PAGINATION_SIZE": pagination_size}

    response = client.get(f"/data/?limit={limit}", **headers)

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "pagination_size,limit,returned_elements_count",
    [
        (10, 10, 10),
        (10, 1, 1),
        # defaults to default limit (aka the page size on the settings)
        (10, -1, 5),
        (20, 11, 11),
        (None, 200, 200),
        (None, 300, 200)
    ],
)
def test_should_return_only_up_to_limit_elements(client, pagination_size, limit, returned_elements_count):
    headers = {"HTTP_X_DRF_MAX_PAGINATION_SIZE": pagination_size}

    response = client.get(f"/data/?limit={limit}", **headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == returned_elements_count


@pytest.mark.django_db
def test_should_work_if_no_limit_is_present(client):
    headers = {"HTTP_X_DRF_MAX_PAGINATION_SIZE": "10"}

    response = client.get(f"/data/", **headers)

    assert response.status_code == status.HTTP_200_OK
