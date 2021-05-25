# DRF Link Navigation Pagination

Yet another [thirdy party package for DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/).

This package adds support to some headers that allow you to configure the behaviour of the LimitOffsetPagination class.

## X-Drf-Change-Domain
If you want to change de host address located on `next` and `previous` fields, then this is the right thing to you. Take this body as an example:

```json
{
  "links": {
    "next": "http://localhost/api/v1/entities/?limit=1&offset=2",
    "previous": "http://localhost/api/v1/entities/limit=1"
  },
  "count": 100,
  "results": [
    {
      "id": "bc6c6868-4e4d-4381-a785-f353ee7ecce5"
    }
  ]
}
```

Using a reverse proxy (like AWS API Gateway) to intermediate between your API, adding `X-Drf-Change-Domain=chumaco` header to the request will make the client receive the following:

```json
{
  "links": {
    "next": "http://chumaco/api/v1/entities/?limit=1&offset=2",
    "previous": "http://chumaco/api/v1/entities/limit=1"
  },
  "count": 100,
  "results": [
    {
      "id": "bc6c6868-4e4d-4381-a785-f353ee7ecce5"
    }
  ]
}
```
## X-Drf-Max-Pagination-Size
This header allows you to define different limits to the pagination depending on the gateway you are exposing your API.
For example. For **client A** we allow a max of `50` entries, for **client B** we allow a max of `100` you can by injecting 
this header on the client's requests.

If for some reason the client exceeds the limit he will receive a Bad Request Error:
```json
{
    "detail": "Bad limit value sent.",
    "error": {
        "code": "bad_limit_value"
    },
    "type": "API_EXCEPTION"
}
```

Otherwise the default paginated  response is generated:
```json
{
  "links": {
    "next": "https://chumaco/api/v1/entities/?limit=1&offset=2",
    "previous": "https://chumaco/api/v1/entities/limit=1"
  },
  "count": 100,
  "results": [
    {
      "id": "bc6c6868-4e4d-4381-a785-f353ee7ecce5"
    }
  ]
}
```

# Configuration process

To use this package after installing you need to use it's pagination class. in your `settings.py` do the following:
```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "drf_link_navigation_pagination.LinkNavigationPagination",
    ...
}
```

## Tests

In order to execute the tests:

    pipenv run tox
