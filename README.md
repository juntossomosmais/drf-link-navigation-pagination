# DRF Link Navigation Pagination

Yet another [thirdy party package for DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/). 

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

Using a reverse proxy (like AWS API Gateway) to intermediate between your API, adding `X-Drf-Change-Domain=chumaço` header to the request will make the client receive the following:

```json
{
  "links": {
    "next": "http://chumaço/api/v1/entities/?limit=1&offset=2",
    "previous": "http://chumaço/api/v1/entities/limit=1"
  },
  "count": 100,
  "results": [
    {
      "id": "bc6c6868-4e4d-4381-a785-f353ee7ecce5"
    }
  ]
}
```

## Tests

In order to execute the tests:

    pipenv run tox
