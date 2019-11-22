from urllib.parse import urlparse

from rest_framework.pagination import LimitOffsetPagination


class LinkNavigationPagination(LimitOffsetPagination):
    def get_paginated_response(self, data, *args, **kwargs):
        paginated_response_from_super = super().get_paginated_response(data)

        next_page = paginated_response_from_super.data["next"]
        previous_page = paginated_response_from_super.data["previous"]
        new_domain = self.request.headers.get("X-Drf-Change-Domain")

        if new_domain:
            paginated_response_from_super.data["next"] = _update_url_otherwise_none(next_page, new_domain)
            paginated_response_from_super.data["previous"] = _update_url_otherwise_none(previous_page, new_domain)

        return paginated_response_from_super


def _get_updated_url(url: str, domain: str) -> str:
    parse_result = urlparse(url)
    # See more about _replace method here: https://docs.python.org/3/library/urllib.parse.html#url-parsing
    new_parse_result = parse_result._replace(netloc=domain)
    return new_parse_result.geturl()


def _update_url_otherwise_none(url: str, domain: str):
    return _get_updated_url(url, domain) if url else None
